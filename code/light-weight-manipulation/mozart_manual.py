import numpy as np
import argparse
import cv2 as cv
import os


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


def main():
    # Training settings
    parser = argparse.ArgumentParser(description='Light weight phase manipulation for Mozart')
    parser.add_argument('--function', type=int, default=1,
                        help='choose manipulation functions')
    parser.add_argument('--redistribution', type = int, default = 1, 
    					help = 'choose a proper function for redistribute outliers')

    args = parser.parse_args()
    



if __name__ == '__main__':
    main()