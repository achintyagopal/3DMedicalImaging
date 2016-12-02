# Paul
import dicom
import numpy as np
from images import *
from threshold import threshold

directory = '../../DOI/0522c0002/set1/pics/'

output_img = threshold(directory)

for x in xrange(len(output_img)):
	show_image(output_img[x], ms=200)