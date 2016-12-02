from images import *
from threshold import *
from marchingCubes import *

directory = '../../../DOI/0522c0002/set1/pics/'

output_img = threshold(directory)
marching_cubes(output_img, 'something.obj')
