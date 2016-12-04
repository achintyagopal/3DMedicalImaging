import numpy as np
import cv2
import math
import numpy.linalg as la
import scipy.optimize as sopt


def project_mesh(points, faces, shape):
	"""
	Method to Project front of a mesh to a 2d image.
	Params:
		list of points
		list of mesh faces
		shape of new img

	Returns:
		numpy array of projection.
	"""
	z, y, x = shape
	img = np.zeros((2 * z, 2 * x))


	# max y
	# multi points by 2

	for face in faces:
		for index in face:
			px, py, pz = points[index]
			px *= 2
			py = 2 * y - py + 1
			pz *= 2

			val = img.item(pz, px)

			if val == 0:
				img.itemset((pz, px), py)
			elif val < py:
				img.itemset((pz, px), py)
	

	max_val = np.amax(img)
	img = img * float(255 / max_val)
	return np.array(img, dtype=np.uint16)





def smooth_projection(img, scale = 700, ker = 4):
	"""
	Smooths a projection.
	Params:
		img - 16 bit image from project_mesh
		scale - OPTIONAL - contrast scaling
		ker - OPTIONAL - Kernel size for Closing op.
	Returns:
		smooth image.
	"""
	tmp = img.copy()
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(ker,ker))
	tmp = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
	tmp = scale * tmp
	return tmp



def laplacian(img):
    """
    Applies the Laplcian operator (2nd order derivative)
    """
    lap = cv2.Laplacian(img, cv2.CV_64F)
    return lap


def sobelx(img, ksize=5):
    """
    Applies a Sobel Kernel in the X Direction
    Derivative in X Dir
    """
    sx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=ksize)
    return sx


def sobely(img, ksize=5):
    """
    Applies a Sobel Kernel in the Y Direction
    Derivative in Y Dir
    """
    sy = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=ksize)
    return sy


def getWindow(img, pos, window = (15,15)):
	y1, x1 = pos

	ySize, xSize = img.shape[:2]
	w = window[0] / 2
	yL = max(0, y1 - w)
	xL = max(0, x1 - w)
	xR = min(xSize, x1 + w + 1)
	yR = min(ySize, y1 + w + 1)
	patch = img[yL:yR, xL:xR].copy() #Find Coord
	return patch




def gradient_descent(img, iteration = 10, gamma = 0.01, win = 15):
	color = cv2.cvtColor(np.array(img * 255.0 / np.amax(img), dtype=np.uint8), cv2.COLOR_GRAY2RGB)
	max_y, max_x = img.shape


	# Nose
	
	parts = {}

	minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(img)
	cv2.circle(color, maxLoc, 1, (255, 0, 255), 5)
	parts["Global_Max"] = maxLoc

	img = img.copy()
	img[img==0] = 65535
	
	win_center = win / 2

	start = (maxLoc[1], maxLoc[0]-20)
	local_min_x = 0
	local_min_y = 0
	count = 0
	while (local_min_x != win_center or local_min_y != win_center):
		if count == iteration:
			print "END ON INTER"
			break
		#         Y    X
		# Get 15x15 window around patch

		patch = getWindow(img, start, window = (win, win))
		# Get max and min (REMEBER X and Y are flipped here.)
		minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(patch)
		local_min_x, local_min_y = minLoc
		new_y = local_min_y - win_center + start[0]
		new_x = local_min_x - win_center + start[1]
		cv2.line(color, (start[1], start[0]), (new_x, new_y), (255, 56, 45), 4)
		start = (new_y, new_x)
		count += 1
		
		

	cv2.circle(color, (start[1], start[0]), 1, (255, 56, 45), 5)
	
	start = (parts["Global_Max"][1], parts["Global_Max"][0]+20)
	local_min_x = 0
	local_min_y = 0
	count = 0
	# for each start point -> make random set of points.
	while (local_min_x != win_center or local_min_y != win_center):
		if count == iteration:
			print "END ON INTER"
			break
		#         Y    X
		# Get 15x15 window around patch

		patch = getWindow(img, start, window = (win, win))
		# Get max and min (REMEBER X and Y are flipped here.)
		minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(patch)
		local_min_x, local_min_y = minLoc
		new_y = local_min_y - win_center + start[0]
		new_x = local_min_x - win_center + start[1]
		cv2.line(color, (start[1], start[0]), (new_x, new_y), (100, 255, 60), 4)
		start = (new_y, new_x)
		count += 1	
	
	cv2.circle(color, (start[1], start[0]), 1, (0, 255, 0), 5)


	return color






