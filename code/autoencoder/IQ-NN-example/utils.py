import os
import cv2
import torch
import time
from torch import nn
from skimage import io
import numpy as np
from torch.utils.data import Dataset
import torch.nn.functional as F
from sklearn import preprocessing
from skimage.metrics import structural_similarity as ssim
from piqa import SSIM
# from torchvision import transforms


class SoftHistTorch(nn.Module):
    def __init__(self, bins, min, max, sigma):
        super(SoftHistTorch, self).__init__()
        self.bins = bins
        self.min = min
        self.max = max
        self.sigma = sigma
        self.delta = float(max - min) / float(bins)
        self.centers = float(min) + self.delta * (torch.arange(bins).float() + 0.5)

    def forward(self, x):

        device = (torch.device('cuda')
          if x.is_cuda
          else torch.device('cpu'))
        self.centers = self.centers.to(device)

        x = torch.unsqueeze(x, 0) - torch.unsqueeze(self.centers, 1)
        x = torch.sigmoid(self.sigma * (x + self.delta/2)) - torch.sigmoid(self.sigma * (x - self.delta/2))
        x = x.sum(dim=1)
        return x


def color_uniform(x):

    flat_x = x.view(x.size(0), -1)#[16, 480 * 640], grad_fn=<ViewBackward0>
    # print("flat_x:", flat_x)

    uniform_loss = 0
    for frame_id in range(flat_x.shape[0]):
        softhist = SoftHistTorch(bins=256, min=0, max=1, sigma=3)
        hist = softhist(flat_x[frame_id])
        entropy = torch.zeros(hist.shape[0])
        for h_id in range(hist.shape[0]):
            if hist[h_id] > 0:
                entropy[h_id] = - hist[h_id] * torch.log(hist[h_id])

        # hist = torch.histc(flat_x[frame_id], bins=256, min=0, max=1)
        # print("hist:", hist)
        # print(entropy.shape)
        # print(torch.max(entropy))
        # print(torch.min(entropy))

        uniform_loss += 0 - torch.sum(entropy)

    uniform_loss /= x.size(0)

    return uniform_loss  


# loss function
class SoftHistogram(nn.Module):
    def __init__(self, w1, w2, w3, bins=100, min=0, max=1, sigma=30):
        super(SoftHistogram, self).__init__()

        self.w1, self.w2, self.w3 = w1, w2, w3

    def forward(self, x, target, depth):

        # print(x.shape)#torch.Size([16, 1, 480, 640])
        # print(target.shape)#torch.Size([16, 480, 640])
        # print(depth.shape)#torch.Size([16, 480, 640])

        x = torch.squeeze(x, 1)#[16, 480, 640]
        # x = F.normalize(x)
        # target = F.normalize(target)
        # depth = F.normalize(depth)

        output = x
        IR = target
        output -= output.clone().min()
        output /= output.clone().max()
        IR -= IR.clone().min()
        IR /= IR.clone().max()
        depth -= depth.clone().min()
        depth /= depth.clone().max()

        # print(torch.max(output))
        # print(torch.min(output))
        # print(torch.max(IR))
        # print(torch.min(IR))

        uniform_loss = color_uniform(output)#Color Space Uniformity
        depth_loss = torch.sum((x * depth).view(-1)) / x.size(0) #Light Field Uniformity using depth maps, * is element-wise product

        output = output.unsqueeze(1)
        IR = IR.unsqueeze(1)
        # print("output, IR:", output.shape, IR.shape)

        ssim = SSIM(n_channels=1).cuda()
        ssim_loss = 1 - ssim(output, IR)

        # loss = ssim_loss
        # loss = self.w1 * 1e-6 * uniform_loss
        # loss = self.w2 * 1e-5 * depth_loss

        print("uniform_loss:", uniform_loss)
        print("depth_loss:", depth_loss)
        print("ssim_loss:", ssim_loss)

        loss = self.w1 * 1e-6 * uniform_loss + self.w2 * 1e-5 * depth_loss + self.w3 * ssim_loss 
        print("loss:", loss)
        # print("x:", x)
        # print("target:", target)

        return loss


class Smoothness(nn.Module):
    def __init__(self, w1=.5, w2=.5):
        super(Smoothness, self).__init__()
        self.l2 = w1
        self.smooth = w2

    def forward(self, x, target, depth):
        l2_loss = torch.mean(torch.square(x - target))

        alpha = 1.2
        lamda = 1.5

        I = target
        L = torch.log(I + 1e-4)
        dx = L[:, :, 1:, :-1] - L[:, :, 1:, 1:]
        dy = L[:, :, :-1, 1:] - L[:, :, 1:, 1:]
        # print('dx  :  {}  | dy  :  {}'.format(dx.shape, dy.shape))
        dx = lamda / (torch.pow(torch.abs(dx), alpha) + 1e-4)
        dy = lamda / (torch.pow(torch.abs(dy), alpha) + 1e-4)
        S = x
        x_loss = dx * torch.pow(S[:, :, 1:, :-1] - S[:, :, 1:, 1:], 2)
        y_loss = dy * torch.pow(S[:, :, :-1, 1:] - S[:, :, 1:, 1:], 2)
        tv_loss = torch.mean(x_loss + y_loss)

        return self.l2 * l2_loss + self.smooth * tv_loss



class AverageMeter(object):
    """Computes and stores the average and current value"""
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count

def hist_equ(im):
    imhist, bins = np.histogram(im.flatten(), 256)
    cdf = imhist.cumsum()
    cdf = 255.0 * cdf / cdf[-1]
    im2 = np.interp(im.flatten(), bins[:-1], cdf)
    im2 = im2.reshape(im.shape)
    # cv.imwrite('tmp2.png',im2)
    return im2
    
def test(model, loader, output_dir):

    model.eval()
    start = time.time()
    for i, (x, target, depth, frame_id) in enumerate(loader):
        x = x.to('cuda')
        output = model(x)
        print(output.shape)
        print(frame_id)

        for j in range(output.shape[0]):
            output_j = output[j].squeeze_().cpu().detach().numpy()
            output_j = (255 * (output_j - np.min(output_j)) / np.ptp(output_j)).astype('uint8')
            cv2.imwrite((os.path.join(output_dir, '{:d}.png'.format(frame_id[j]))), hist_equ(output_j))

        print("time cost: ", time.time() - start)


def train(model, train_loader, criterion, optimizer, epochs, model_folder):
    model.train()
    total_loss = []

    running_loss = AverageMeter()

    for epoch in range(epochs):
        t = time.time()
        for i, (x, target, depth, frame_id) in enumerate(train_loader):

            x, target, depth = x.to("cuda"), target.to("cuda"), depth.to("cuda")
            bsz = x.shape[0]

            optimizer.zero_grad()
            outputs = model(x)
            loss = criterion(outputs, target, depth)#torch.Size([16, 480, 640])
            loss.backward()
            optimizer.step()
            running_loss.update(loss.item(), bsz)

            if (i + 1) % 2 == 0:
                print('\r', 'Epoch: {:04d}, '.format(epoch + 1), '\t',  'Batch {:04d}/{:04d}, '.format(i+1, len(train_loader)), '\t',
                    'loss {loss.val:.3f} ({loss.avg:.3f})'.format(loss=running_loss), '\t', 'time: {:.6f}s'.format(time.time() - t), '\n',flush=True, end='')
        total_loss.append(running_loss.avg)

        if (epoch % 10) == 0:
            torch.save(model.state_dict(), model_folder + 'epoch_{:d}.pth'.format(epoch))
    
    torch.save(model.state_dict(), model_folder + 'last.pth'.format(epoch))
        # loss_val = test(model, val_loader, criterion)
        # print('\n', 'loss_train: {:.6f}'.format(loss_val))

    return model, total_loss
