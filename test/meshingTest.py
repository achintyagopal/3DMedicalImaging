from images import *
from threshold import *
from marchingCubes import *

directory = './images/'
#directory = '../../../DOI/0522c0001/set3/pics/'

output_img, thickness, spacing = threshold(directory)
marching_cubes(output_img, spacing, thickness, 'something_part2.obj')
