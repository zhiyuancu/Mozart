import os
import torch
import cv2
from model import EncoderNet
from utils import *
import time
from torch.utils.data import DataLoader, random_split
from data_pre import *
import sys

# from torchvision.utils import save_image


data_source = str(sys.argv[1])
data_folder = '../' + data_source
model_folder = './save/' + data_source + 'save-325/'

iq_dir = data_folder + 'IQ/'
target_dir = data_folder + 'IR/'
depth_dir = data_folder + 'depth-fastN/'
output_dir = './save/' + data_source + 'output-325-20/'

model_path = model_folder +'last.pth'
print(model_path)
batch_size = 4

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def hist_equ(im):
    imhist, bins = np.histogram(im.flatten(), 256)
    cdf = imhist.cumsum()
    cdf = 255.0 * cdf / cdf[-1]
    im2 = np.interp(im.flatten(), bins[:-1], cdf)
    im2 = im2.reshape(im.shape)
    # cv.imwrite('tmp2.png',im2)
    return im2


if __name__ == '__main__':

    dataset = IQ_dataset(iq_dir, target_dir, depth_dir)
    num = len(dataset)
    print("num of samples:", num)

    test_num = int(num * 0.999)
    train_num = num - test_num
    train_data, test_data = random_split(
        dataset, [train_num, test_num], generator=torch.Generator().manual_seed(42))

    test_loader = DataLoader(test_data, batch_size=batch_size)

    model = EncoderNet()#.to('cuda:0')
    if torch.cuda.device_count() > 1:
        model = torch.nn.DataParallel(model)
    model = model.cuda()
    model.load_state_dict(torch.load(model_path))

    model.eval()
    start = time.time()

    record_frame_num = 0
    for i, (x, target, depth, frame_id) in enumerate(test_loader):

        x = x.to('cuda')
        output = model(x)
        print(output.shape)
        print(frame_id)
        record_frame_num += frame_id.shape[0]
        print("record_frame_num: ",record_frame_num)

        record_frame_num_batch = 0
        for j in range(output.shape[0]):
            output_j = output[j].squeeze_().cpu().detach().numpy()
            output_j = (255 * (output_j - np.min(output_j)) / np.ptp(output_j)).astype('uint8')
            cv2.imwrite((os.path.join(output_dir, '{:d}.png'.format(frame_id[j]))), hist_equ(output_j))
            print(frame_id[j])
            record_frame_num_batch+=1
            print("record_frame_num_batch: ",record_frame_num_batch)

        # print("time cost: ", time.time() - start)
