# Paul
import dicom
import numpy as np
from images import *
from threshold import threshold
'''
directory = '../../DOI/0522c0001/set3/pics/'


before_img, output_img, _, _ = threshold(directory)

for x in xrange(len(output_img)):
	cv2.imwrite("./gifs/ret1_%03d.jpg" % x, output_img[x])
	cv2.imwrite("./gifs/bef1_%03d.jpg" % x, before_img[x])
	#show_image(output_img[x], ms=100)
'''
directory = '../../DOI/0522c0817/set1/pics/'

before_img, output_img, _, _ = threshold(directory)

for x in xrange(len(output_img[0][0])):
	#cv2.imwrite("./gifs/ret2_%03d.jpg" % x, output_img[x])
	#cv2.imwrite("./gifs/bef2_%03d.jpg" % x, before_img[x])
	# rows, cols = output_img[:,:,x].shape[:2]
	# output_img[:,:,x]
	# img = cv2.resize(output_img[:,:,x], (rows*5, cols))
	show_image(output_img[:,:,x], ms=50)
	# show_image(img, ms=50)

'''
directory = '../../DOI/0522c0419/set2/pics/'

before_img, output_img, _, _ = threshold(directory)

for x in xrange(len(output_img)):
	cv2.imwrite("./gifs/ret3_%03d.jpg" % x, output_img[x])
	cv2.imwrite("./gifs/bef3_%03d.jpg" % x, before_img[x])
	#show_image(output_img[x], ms=100)
'''
