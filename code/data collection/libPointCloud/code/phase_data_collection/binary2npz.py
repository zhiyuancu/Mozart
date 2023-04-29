import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from PIL import Image
import struct
import sys

if len(sys.argv) != 3:
	sys.exit()

file_num = int(sys.argv[2])

for i in range(file_num):
	print(i)
	for j in range(1,5):
		phase_path = "./" + str(sys.argv[1]) + "/frame_"+str(i)+"_"+str(j)+".txt"
		save_path = "./" + str(sys.argv[1]) + "/frame_"+str(i)+"_"+str(j)+".npz"

		numerFile = open(phase_path,"rb")
		phase = np.zeros((480,640))

		for x in range(480):
			for y in range(640):
				context = numerFile.read(2)
				phase[x][y] = struct.unpack("h",context)[0]
				# print(realContext)

		# phase = phase.astype('short')
		np.savez_compressed(save_path,data = phase)
