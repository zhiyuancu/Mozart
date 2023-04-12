import numpy as np
import cv2
import sys
import os
from PIL import Image

if len(sys.argv) != 3:
	print("Usage: python ConvertPhase.py folder_name file_num")
	sys.exit()


file_num = int(sys.argv[2])

if not os.path.exists("./" + str(sys.argv[1]) + "/phase/"):
	os.makedirs("./" + str(sys.argv[1]) + "/phase/")

for i in range(1, file_num+1):
	depth_path = "./" + str(sys.argv[1]) + "/depth/"+str(i) + ".png"
	ir_path = "./" + str(sys.argv[1]) + "/ir/"+str(i) + ".png"

	save1 = str(sys.argv[1]) + "/phase/phase_" + str(i) + "_1.npz"
	save2 = str(sys.argv[1]) + "/phase/phase_" + str(i) + "_2.npz"

	depth = Image.open(depth_path)
	depth = np.array(depth)
	ir = Image.open(ir_path)
	ir = np.array(ir)

	depth[depth == 65535] = 0 

	N2 = ir * depth / 4444
	N1 = ir * (1 - depth / 4444)

	N2 = N2 / 100
	N1 = N1 / 100

	np.savez_compressed(save1, data = N1)
	np.savez_compressed(save2, data = N2)
