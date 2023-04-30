import numpy as np
from torch.utils.data import Dataset
import torch
import os
from skimage import io
# from sklearn.model_selection import train_test_split
# import random


MEAN_OF_I = 0.6247411913278113
STD_OF_I = 8.299889463721907

MEAN_OF_Q = 1.5035214381832886
STD_OF_Q = 5.250668825141449

MEAN_OF_IR = 65.76613814197763
STD_OF_IR = 65.79431242448139

MEAN_OF_depth = 90.29070453253988
STD_OF_depth = 75.83449327878687
# random.seed(0)


def getFrameId(path):
    print("platform_1!!!!!!!!!!!!")
    files = [f for f in os.listdir(path) if f.endswith('png')]
    frames = [int(name.split('.')[0]) for name in files]
    return frames

def hist_equ(im):
    imhist, bins = np.histogram(im.flatten(), 256)
    cdf = imhist.cumsum()
    cdf = 255.0 * cdf / cdf[-1]
    im2 = np.interp(im.flatten(), bins[:-1], cdf)
    im2 = im2.reshape(im.shape)
    # cv.imwrite('tmp2.png',im2)
    return im2
    
class IQ_dataset(Dataset):
    def __init__(self, iq_dir, target_dir, depth_dir):
        self.iq_dir = iq_dir
        self.target_dir = target_dir
        self.depth_dir = depth_dir
        self.frames = getFrameId(depth_dir)
        print(self.frames)


    def __len__(self):
        return int(len(self.frames))

    def __getitem__(self, idx):

        frame_id = self.frames[idx]
        ii = np.loadtxt(os.path.join(self.iq_dir, '{:d}_I.txt'.format(frame_id)))
        iq = np.loadtxt(os.path.join(self.iq_dir, '{:d}_Q.txt'.format(frame_id)))

        ii = (ii - MEAN_OF_I) / STD_OF_I
        iq = (iq - MEAN_OF_Q) / STD_OF_Q

        item = torch.from_numpy(np.array([ii, iq]).astype(np.float32))

        # print("IQ shape: ",item.shape)#IQ shape:  torch.Size([2, 480, 640])

        target = io.imread(os.path.join(self.target_dir, '{:d}.png'.format(frame_id)))
        target = (target - MEAN_OF_IR) / STD_OF_IR
        target = torch.from_numpy(target.astype(np.float32))

        # print("IR shape: ",target.shape)#IR shape:  torch.Size([480, 640])
        # target = target.view(1, target.shape[0], target.shape[1])

        depth = io.imread(os.path.join(self.depth_dir, '{:d}.png'.format(frame_id)))
        depth = (depth - MEAN_OF_depth) / STD_OF_depth
        depth = torch.from_numpy(depth.astype(np.float32))
        
        # print("depth shape: ",depth.shape)#depth shape:  torch.Size([480, 640])

        return item, target, depth[:,:,0], frame_id
        

# dir = './data/depth-fastN/'

# # num_of_frames = len(getFrameId(dir))
# # print(num_of_frames)
# num_of_frames = 684

# i_list = []

# # for I and Q
# # for frame_id in range(int(num_of_frames)):
# # 	i_list.append( np.loadtxt(os.path.join(dir, '{:d}_I.txt'.format(frame_id))) )

# # for IR or IR-equ
# for frame_id in range(int(num_of_frames)):
# 	i_list.append( io.imread(os.path.join(dir, '{:d}.png'.format(frame_id))) )

# i_array = np.array(i_list)
# print(i_array.shape)#(188, 480, 640)

# print("mean:", np.mean(i_array))
# print("std:", np.std(i_array))
