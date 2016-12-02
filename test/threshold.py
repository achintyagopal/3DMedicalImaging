# Paul
import dicom
import numpy as np
import os
import pickle
from images import *


def threshold(directory):

	real_output_img = []
	index = 0
	for filename in os.listdir(directory):
		if filename.endswith(".dcm"):
			RefDs = dicom.read_file(directory + filename)
			ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns))
			ConstPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]))

			x = np.arange(0.0, (ConstPixelDims[0]+1)*ConstPixelSpacing[0], ConstPixelSpacing[0])
			y = np.arange(0.0, (ConstPixelDims[1]+1)*ConstPixelSpacing[1], ConstPixelSpacing[1])

			ArrayDicom = np.zeros(ConstPixelDims, dtype=np.int16)
			ArrayDicom[:, :] = RefDs.pixel_array
			ArrayDicom = ArrayDicom * (255/float(np.amax(ArrayDicom)))
			ArrayDicom = np.array(ArrayDicom, dtype=np.uint8)

			#Thresholding
			ret, binary_img = cv2.threshold(ArrayDicom, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

			#Get a window at the center and do sequencial labelling from it, then deleting areas with too small width

			#Get connected components
			num_labels, label_img, stats, centers = cv2.connectedComponentsWithStats(binary_img, 4, cv2.CV_32S)

			# Finding the label of the head
			label_votes = np.zeros(441, dtype=np.int64)
			center_row = int(RefDs.Rows) / 2
			center_col = int(RefDs.Columns) / 2
			count = 0
			for y in xrange(-10, 11):
				for x in xrange(-10, 11):
					vote = label_img.item(y + center_row, x + center_col)
					label_votes.itemset(count, vote)
					count += 1
			head_label = np.bincount(label_votes).argmax()

			#Selecting only the head labeled pixels
			label_img = cv2.inRange(label_img, head_label, head_label)
			#change the size of the kernel to adjust amount of open and dilation
			kernel = np.ones((5, 5), np.uint8)
			label_img = cv2.morphologyEx(label_img, cv2.MORPH_OPEN, kernel)


			label_img = cv2.dilate(label_img, kernel)


			#Getting the pixel values of the original image in the head area
			output_img = cv2.bitwise_and(ArrayDicom, ArrayDicom, mask=label_img)

			#Append slice to 3d arrray
			real_output_img.append(output_img)

	#Stack up all the images into one big 3d array
	finally_real_output_img = np.array(real_output_img)


	return finally_real_output_img