import dicom
import numpy as np
from images import *
from matplotlib import pyplot, cm

path = './'
files = ['000000.dcm']

for file in files:
    RefDs = dicom.read_file(path + file)
    ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns))
    ConstPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]), float(RefDs.SliceThickness))

    x = np.arange(0.0, (ConstPixelDims[0]+1)*ConstPixelSpacing[0], ConstPixelSpacing[0])
    y = np.arange(0.0, (ConstPixelDims[1]+1)*ConstPixelSpacing[1], ConstPixelSpacing[1])

    ArrayDicom = np.zeros(ConstPixelDims, dtype=np.int16)
    ArrayDicom[:, :] = RefDs.pixel_array
    ArrayDicom = ArrayDicom * (255/float(np.amax(ArrayDicom)))
    ArrayDicom = np.array(ArrayDicom, dtype=np.uint8)

    show_image(ArrayDicom)
