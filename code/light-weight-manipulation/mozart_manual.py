import numpy as np
import argparse
import cv2 as cv
import os
import sys
import matplotlib.pyplot as plt

def get_files_with_suffix(folder_path, suffix):
    files = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(suffix):
            files.append(file_name)
    return files

def func1(N1, N2):
	return N2 * N2 / (N1 + N2 + 1e-2)

def func2(N1, N2):
	return N1 * N2 / (N1 + N2 + 1e-2)

def func3(N1, N2):
	return N1 + N2

def func4(N1, N2):
	return N1 * N2


def sigmoid(z):
	return 1 / (1 + np.exp(-z))

def tanh(z):
	return (np.exp(z) - np.exp(-z))/(np.exp(z) + np.exp(-z))

def sqrt(z):
	return np.sqrt(z)


# def load_data(tof_type, )


def main():
    # Training settings
    parser = argparse.ArgumentParser(description='Light weight phase manipulation for Mozart')
    # parser.add_argument('--tof_type', type = int, default = 0, 
    	# help = 'choose the type of ToF cameras, 0 for cwToF, 1 for pToF')
    parser.add_argument('--function', type=int, default=1,
                        help='choose manipulation functions, x for funcx')
    parser.add_argument('--redistribution', type = int, default = 0, 
    					help = 'choose a proper function for redistribute outliers, 0 for sigmoid, ...')

    parser.add_argument('--folder', type=str, default = 'cwToF', help = 'choose the data folder')

    args = parser.parse_args()

    N1_suffix = '1.npz'
    N1_files = get_files_with_suffix(args.folder, N1_suffix)
    file_count = len(N1_files)
    # N2_suffix = '2.npz'
    # N2_files = get_files_with_suffix(args.folder, N2_suffix)
    for i in range(file_count):
    	N1_path = os.path.join(args.folder, "phase_" + str(i) + "_1.npz")
    	N2_path = os.path.join(args.folder, "phase_" + str(i) + "_2.npz")
    	# save_path = os.path.join(args.folder, "Mozart_" + str(i) + ".png")
    	save_path = os.path.join(args.folder, "Mozart_" + str(i) + ".npz")

    	N1 = np.load(N1_path)['data']
    	N2 = np.load(N2_path)['data']

    	if args.function == 1:
    		tmp = func1(N1, N2)
    	elif args.function == 2:
    		tmp = func2(N1, N2)
    	elif args.function == 3:
    		tmp = func3(N1, N2)
    	else:
    		tmp = func4(N1, N2)


    	if args.redistribution == 0:
    		tmp = sigmoid(tmp)
    	elif args.redistribution == 1:
    		tmp = tanh(tmp)
    	else:
    		tmp = sqrt(tmp)

    	np.savez_compressed(save_path, data = tmp)
    	# plt.imshow(tmp, cmap = 'gray')
    	# plt.savefig(save_path)


if __name__ == '__main__':
    main()