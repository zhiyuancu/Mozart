from model import EncoderNet
from utils import *
import numpy as np
import argparse
from torch.utils.data import DataLoader, random_split
from data_pre import *
import torch.backends.cudnn as cudnn

parser = argparse.ArgumentParser()

parser.add_argument('--w1', type=float, default=0.3, help='w1')
parser.add_argument('--w2', type=float, default=0.2, help='w2')
parser.add_argument('--w3', type=float, default=0.5, help='w3')
parser.add_argument('--epochs', type=int, default=100, help='epochs')
parser.add_argument('--batch_size', type=int, default=16, help='batch_size')
parser.add_argument('--lr', type=float, default=1e-3, help='lr')
# parser.add_argument('--output', type=str, default='output-no-uniform/')
parser.add_argument('--source', type=str, default='example_1/')
parser.add_argument('--setting', type=str, default='325')

args = parser.parse_args()

data_source = args.source
data_folder = '../' + data_source
model_folder = './save/' + data_source + 'save-'+ args.setting + "/"
loss_folder = './save/' + data_source + 'loss-'+ args.setting + "/"

if not os.path.exists(model_folder):
    os.makedirs(model_folder)
if not os.path.exists(loss_folder):
    os.makedirs(loss_folder)

iq_dir = data_folder + 'IQ/'
target_dir = data_folder + 'IR/'
depth_dir = data_folder + 'depth-fastN/'
output_dir = './save/' + data_source + 'output-' + args.setting + "/"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    
weight_decay = 0.01
# epochs = 10
# batch_size = 4
# lr = 1e-3

if __name__ == '__main__':

    dataset = IQ_dataset(iq_dir, target_dir, depth_dir)
    w1, w2, w3 = args.w1, args.w2, args.w3

    num = len(dataset)
    print("num of samples:", num)

    test_num = int(num * 0.25)
    train_num = num - test_num
    train_data, test_data = random_split(
        dataset, [train_num, test_num], generator=torch.Generator().manual_seed(42))

    train_loader, test_loader = DataLoader(train_data, batch_size=args.batch_size), DataLoader(test_data, batch_size=args.batch_size)

    model = EncoderNet()#.to('cuda:0')
    loss_func = SoftHistogram(w1, w2, w3)
    opt = torch.optim.Adam(model.parameters(), lr=args.lr, weight_decay=weight_decay)

    if torch.cuda.device_count() > 1:
        model = torch.nn.DataParallel(model)
    model = model.cuda()
    loss_func = loss_func.cuda()
    cudnn.benchmark = True
    
    # #train
    model, loss = train(model, train_loader, loss_func, opt, args.epochs, model_folder)
    np.savetxt(loss_folder + "ssim_loss.txt", np.array(loss))

    # torch.save(model.state_dict(), 'tracking_epoch_{:d}.pth'.format(args.epochs))

    # # test
    test(model, test_loader, output_dir)

    # model.eval()
    # start = time.time()
    # for i, (x, target, depth, frame_id) in enumerate(test_loader):
    #     # x = x.to('cuda:0')
    #     output = model(x)
    #     print(output.shape)
    #     print(frame_id)

    #     for j in range(output.shape[0]):
    #         output_j = output[j].squeeze_().cpu().detach().numpy()
    #         output_j = (255 * (output_j - np.min(output_j)) / np.ptp(output_j)).astype('uint8')
    #         cv2.imwrite((os.path.join(output_dir, '{:d}.png'.format(frame_id[j]))), hist_equ(output_j))

    #     print("time cost: ", time.time() - start)



