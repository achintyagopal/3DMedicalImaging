# Paul
import dicom
import numpy as np
import os
import pickle
from images import *


def threshold(directory):

	print "Threshold"

	real_output_img = []
	index = 0
	before = []
	foundThickness = 0
	SliceThickness = None
	for filename in os.listdir(directory):
		if filename.endswith(".dcm"):
			RefDs = dicom.read_file(os.path.join(directory, filename))

			if SliceThickness is None:
				# print RefDs.ImageOrientationPatient
				SliceThickness = RefDs.ImagePositionPatient[2]
			elif not foundThickness:
				# print RefDs.ImagePositionPatient
				# print ""
				SliceThickness -= RefDs.ImagePositionPatient[2]
				if SliceThickness < 0:
					SliceThickness *= -1
				foundThickness = 1

			
			ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns))
			ConstPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]))
			# print "LOOK HERE", RefDs.SliceThickness, RefDs.PixelSpacing

			x = np.arange(0.0, (ConstPixelDims[0]+1)*ConstPixelSpacing[0], ConstPixelSpacing[0])
			y = np.arange(0.0, (ConstPixelDims[1]+1)*ConstPixelSpacing[1], ConstPixelSpacing[1])

			ArrayDicom = np.zeros(ConstPixelDims, dtype=np.int16)
			# print RefDs.pixel_array.dtype
			ArrayDicom[:, :] = RefDs.pixel_array
			ArrayDicom = ArrayDicom * (255/float(np.amax(ArrayDicom)))
			ArrayDicom = np.array(ArrayDicom, dtype=np.uint8)

			before.append(ArrayDicom)

			#Thresholding
			ret, binary_img = cv2.threshold(ArrayDicom, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

			#Get a window at the center and do sequencial labelling from it, then deleting areas with too small width

			#Get connected components
			num_labels, label_img, stats, centers = cv2.connectedComponentsWithStats(binary_img, 4, cv2.CV_32S)

			# Finding the label of the head
			label_votes = np.zeros(1681, dtype=np.int64)
			center_row = int(RefDs.Rows) / 2
			center_col = int(RefDs.Columns) / 2
			count = 0
			for y in xrange(-20, 21):
				for x in xrange(-20, 21):
					vote = label_img.item(y + center_row, x + center_col)
					if vote == 0:
						continue
					label_votes.itemset(count, vote)
					count += 1

			if count == 0:
				print index
				show_image(ArrayDicom)
			# show_image(binary_img)
			# show_image(label_img)
			head_label = np.bincount(label_votes[:count]).argmax()

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
			index += 1

	#Stack up all the images into one big 3d array
	finally_real_output_img = np.array(real_output_img)

	return finally_real_output_img, SliceThickness
