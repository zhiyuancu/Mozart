import numpy as np
import cv2
import sys

if len(sys.argv) != 3:
	sys.exit()

file_num = int(sys.argv[2])

for i in range(file_num):
	phase_1_path = str(sys.argv[1]) + "/frame_" + str(i) + "_1.npz"
	phase_2_path = str(sys.argv[1]) + "/frame_" + str(i) + "_2.npz"
	phase_3_path = str(sys.argv[1]) + "/frame_" + str(i) + "_3.npz"
	phase_4_path = str(sys.argv[1]) + "/frame_" + str(i) + "_4.npz"
	
	phase_1 = np.load(phase_1_path)['data']
	phase_2 = np.load(phase_2_path)['data']
	phase_3 = np.load(phase_3_path)['data']
	phase_4 = np.load(phase_4_path)['data']

	phase_i = phase_1 - phase_3
	phase_q = phase_2 - phase_4

	amp = np.sqrt(np.power(phase_i, 2) + np.power(phase_q, 2))
	phase = np.arctan2(phase_q, phase_i)
	phase[phase < 0] += 2*np.pi 

	N2 = amp * phase / (2 * np.pi)
	N1 = amp * (1 - phase / (2 * np.pi))

	save1 = str(sys.argv[1]) + "/phase_" + str(i) + "_1.npz"
	save2 = str(sys.argv[1]) + "/phase_" + str(i) + "_2.npz"

	np.savez_compressed(save1, data = N1)
	np.savez_compressed(save2, data = N2)
