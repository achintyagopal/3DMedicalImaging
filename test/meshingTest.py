from images import *
from threshold import *
from marchingCubes import *

directory = '../../DOI/0522c0002/set1/pics/'

output_img = threshold(directory)
marching_cubes(output_img)
# for x in xrange(len(output_img)):
    # show_image(output_img[x], ms=200)
