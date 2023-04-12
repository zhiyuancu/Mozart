import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from PIL import Image
import struct
import sys

if len(sys.argv) != 2:
	sys.exit()

for i in range(2000):
	print(i)
	for j in range(1,5):
		numerator_path = "./" + str(sys.argv[1]) + "/frame_"+str(i)+"_"+str(j)+".txt"
		save_path = "./" + str(sys.argv[1]) + "/frame_"+str(i)+"_"+str(j)+".txt"

		numerFile = open(numerator_path,"rb")
		numerator = np.zeros((480,640))

		for x in range(480):
			for y in range(640):
				context = numerFile.read(2)
				numerator[x][y] = struct.unpack("h",context)[0]
				# print(realContext)

		# numerator = numerator.astype('short')
		np.savetxt(save_path,numerator,fmt='%d')
