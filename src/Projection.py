import numpy as np
import cv2
from images import *
import math


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

			px = int(px)
			py = int(py)
			pz = int(pz)
			
			val = img.item(pz, px)

			if val == 0:
				img.itemset((pz, px), py)
			elif val < py:
				img.itemset((pz, px), py)
	

	max_val = np.amax(img)
	img = img * float(255 / max_val)
	
	return np.array(img, dtype=np.uint16)


def project_mesh_profile(points, faces, shape):
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
	img = np.zeros((2 * z, 2 * y))


	# max y
	# multi points by 2

	for face in faces:
		for index in face:
			px, py, pz = points[index]
			py *= 2
			px = 2 * y - px + 1
			pz *= 2

			px = int(px)
			py = int(py)
			pz = int(pz)
			
			val = img.item(pz, py)

			if val == 0:
				img.itemset((pz, py), px)
			elif val < px:
				img.itemset((pz, py), px)
	

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

	# print window
	y1, x1 = pos

	ySize, xSize = img.shape[:2]
	w = window[0] / 2
	yL = max(0, y1 - w)
	xL = max(0, x1 - w)
	xR = min(xSize, x1 + w + 1)
	yR = min(ySize, y1 + w + 1)
	patch = img[yL:yR, xL:xR].copy() #Find Coord
	return patch


def getRightWindow(img, pos, window = (15,15)):

	# print window
	y1, x1 = pos

	ySize, xSize = img.shape[:2]
	w = window[0]
	yL = max(0, y1 - 1)
	xL = max(0, x1 - 1)
	xR = min(xSize, x1 + w)
	yR = min(ySize, y1 + w)
	patch = img[yL:yR, xL:xR].copy() #Find Coord
	return patch



def getLeftWindow(img, pos, window = (15,15)):

	# print window
	y1, x1 = pos

	ySize, xSize = img.shape[:2]
	w = window[0]
	yL = max(0, y1 - w)
	xL = max(0, x1 - w)
	xR = min(xSize, x1 + 2)
	yR = min(ySize, y1 + 2)
	patch = img[yL:yR, xL:xR].copy() #Find Coord
	return patch


def gradient_descent(img, iteration = 10, gamma = 0.01, win = 15):
	color = cv2.cvtColor(np.array(img * 255.0 / np.amax(img), dtype=np.uint8), cv2.COLOR_GRAY2RGB)
	max_y, max_x = img.shape
	tmp = color.copy()
	# Nose
	
	parts = {}

	img[:,:img.shape[1]/2 - 40] = 0
	img[:,img.shape[1]/2 + 40:] = 0
	minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(img)
	# cv2.circle(color, maxLoc, 1, (255, 0, 255), 5)
	# cv2.rectangle(color, (maxLoc[0] - 80, maxLoc[1] - 20), (maxLoc[0] + 80, maxLoc[1] + 20), (0,0,255), 3 )

	# img[maxLoc[1] - 20:maxLoc[1] + 20, maxLoc[0] - 80:maxLoc[0] + 80] = 0
	# minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(img)
	# cv2.circle(color, maxLoc, 1, (255, 0, 255), 5)
	# cv2.rectangle(color, (maxLoc[0] - 80, maxLoc[1] - 20), (maxLoc[0] + 80, maxLoc[1] + 20), (0,0,255), 3 )

	# img[maxLoc[1] - 20:maxLoc[1] + 20, maxLoc[0] - 80:maxLoc[0] + 80] = 0
	# minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(img)
	# cv2.circle(color, maxLoc, 1, (255, 0, 255), 5)
	# cv2.rectangle(color, (maxLoc[0] - 80, maxLoc[1] - 20), (maxLoc[0] + 80, maxLoc[1] + 20), (0,0,255), 3 )

	# show_image(color)
	# return

	parts["Nose"] = maxLoc

	img = img.copy()
	img[img==0] = 65535
	
	win_center = win / 2

	start = (maxLoc[1] - 20, maxLoc[0]-20)
	local_min_x = 0
	local_min_y = 0
	count = 0
	winTmp = win
	while (local_min_x != win_center or local_min_y != win_center):
		if count == iteration:
			print "END ON INTER"
			break
		#         Y    X
		# Get 15x15 window around patch
		# print win
		win_center = win / 2
		patch = getWindow(img, start, window = (win, win))
		# Get max and min (REMEMBER X and Y are flipped here.)
		minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(patch)
		local_min_x, local_min_y = minLoc
		new_y = local_min_y - win_center + start[0]
		new_x = local_min_x - win_center + start[1]

		# print start
		# print new_y, new_x
		win = int(max(math.fabs(new_x - start[1]), math.fabs(new_y - start[0])))
		# print ""

		cv2.line(color, (start[1], start[0]), (new_x, new_y), (255, 56, 45), 4)
		start = (new_y, new_x)
		count += 1
		
	win = winTmp
	win_center = win / 2
	# cv2.circle(color, (start[1], start[0]), 1, (255, 56, 45), 5)
	parts["Left_eye"] = (start[1], start[0])

	start = (parts["Nose"][1] - 20, parts["Nose"][0]+30)
	local_min_x = 0
	local_min_y = 0
	count = 0
	while (local_min_x != win_center or local_min_y != win_center):
		if count == iteration:
			print "END ON INTER"
			break
		#         Y    X
		# Get 15x15 window around patch
		win_center = win / 2
		# patch = getWindow(img, start, window = (win, win))
		patch = getRightWindow(img, start, window = (win, win))
		# Get max and min (REMEMBER X and Y are flipped here.)
		minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(patch)
		local_min_x, local_min_y = minLoc
		new_y = local_min_y - win_center + start[0]
		new_x = local_min_x - win_center + start[1]

		win = int(max(math.fabs(new_x - start[1]), math.fabs(new_y - start[0])))
		cv2.line(color, (start[1], start[0]), (new_x, new_y), (100, 255, 60), 4)
		start = (new_y, new_x)
		count += 1	
	
	# show_image(color)

	# cv2.circle(color, (start[1], start[0]), 1, (0, 255, 0), 5)
	parts["Right_eye"] = (start[1], start[0])

	cv2.circle(color, (parts["Right_eye"][0] + 30, parts["Right_eye"][1] + 5), 1, (255,56,45), 2)
	cv2.circle(color, (parts["Left_eye"][0] - 30, parts["Left_eye"][1] + 5), 1, (255,56,45), 2)
	cv2.circle(color, (parts["Nose"][0], parts["Nose"][1]), 1, (255,56,45), 2)

	show_image(color)


	flood = floodFill(tmp, (parts["Nose"][0], parts["Nose"][1]), val=(255,0,0), lo=11, hi=11, fixedRng=True)

	tmp2 = flood.copy()
	yPos = parts["Right_eye"][1] + 5
	flood[:yPos - 15] = 0
	flood[yPos + 15:] = 0

	tmp2[yPos - 15: yPos + 15] = 0

	flood = floodFill(flood, (parts["Right_eye"][0] + 30, parts["Right_eye"][1] + 3), val=(0,255,0), lo=0, hi=0)
	flood = tmp2 + flood

	tmp2 = flood.copy()
	yPos = parts["Left_eye"][1] + 5
	flood[:yPos - 15] = 0
	flood[yPos + 15:] = 0
	tmp2[yPos - 15: yPos + 15] = 0

	flood = floodFill(flood, (parts["Left_eye"][0] - 30, parts["Left_eye"][1] + 5), val=(0,0,255), lo=0, hi=0)
	flood = tmp2 + flood

	show_image(flood)

	right_eye_mask = cv2.inRange(flood, (0,254,0), (0,255,0))

	# yPos = parts["Right_eye"][1] + 5
	# right_eye_mask[:yPos - 20] = 0
	# right_eye_mask[yPos + 20:] = 0
	# right_eye_mask = cv2.erode(right_eye_mask, iterations=2, kernel=np.ones((5,5)))
	left_eye_mask = cv2.inRange(flood, (0,0,254), (0,0,255))
	# yPos = parts["Left_eye"][1] + 5
	# right_eye_mask[:yPos - 20] = 0
	# right_eye_mask[yPos + 20:] = 0
	# # left_eye_mask = cv2.erode(left_eye_mask, iterations=2, kernel=np.ones((5,5)))
	nose_mask = cv2.inRange(flood, (254,0,0), (255,0,0))
	# # nose_mask = cv2.erode(nose_mask, iterations=1, kernel=np.ones((5,5)))
	# show_image(right_eye_mask)
	# return
	_, right_contours, _ = cv2.findContours(right_eye_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	right_contours = sorted(right_contours, key=lambda x : cv2.contourArea(x), reverse=True)
	# print right_contours
	# right_ellipse = cv2.fitEllipse(right_contours[0])
	# print right_ellipse
	# cv2.ellipse(color, right_ellipse, (0,255,0), 2)

	_, left_contours, _ = cv2.findContours(left_eye_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	left_contours = sorted(left_contours, key=lambda x : cv2.contourArea(x), reverse=True)
	# left_ellipse = cv2.fitEllipse(left_contours[0])
	
	# cv2.ellipse(color, left_ellipse, (0,0,255), 2)

	_, nose_contours, _ = cv2.findContours(nose_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	nose_contours = sorted(nose_contours, key=lambda x : cv2.contourArea(x), reverse=True)
	nose_ellipse = cv2.fitEllipse(nose_contours[0])
	left_eye_mask = cv2.cvtColor(left_eye_mask, cv2.COLOR_GRAY2RGB)
	if len(right_contours) == 0:
		y1, x1 = centroid(left_contours[0])
		y2, x2 = centroid(left_contours[1])
		if x1 < x2:
			right_ellipse = cv2.fitEllipse(left_contours[0])
			left_ellipse = cv2.fitEllipse(left_contours[1])
			cv2.drawContours(tmp, [nose_contours[0], left_contours[0], left_contours[1]], -1, color=(255, 100, 3), thickness=4)

		else:
			right_ellipse = cv2.fitEllipse(left_contours[1])
			left_ellipse = cv2.fitEllipse(left_contours[0])
			cv2.drawContours(tmp, [nose_contours[0], left_contours[0], left_contours[1]], -1, color=(255, 100, 3), thickness=4)

	else:
		left_ellipse = cv2.fitEllipse(left_contours[0])
		right_ellipse = cv2.fitEllipse(right_contours[0])
		cv2.drawContours(tmp, [nose_contours[0], left_contours[0], right_contours[0]], -1, color=(255, 100, 3), thickness=4)

	# show_image(tmp)

	# cv2.ellipse(color, nose_ellipse, (255,0,0), 2)

	return right_ellipse, left_ellipse, nose_ellipse

def centroid(contour):
	M = cv2.moments(contour)
	cx = int(M['m10']/M['m00'])
	cy = int(M['m01']/M['m00'])
	return cy, cx

def floodFill(img, seedPoint, val=(255,255,255), lo=25, hi=25, fixedRng=False, connectivity=4):
	"""
	Flood Fill Algorithm
	Params:
		* img - image
		* seedPoint - startPoint
		* val -OPTIONAL - New Value; 255,255,255
		* lo - OPTIONAL - Max lower birghtness/color diff; def: 20
		* hi - OPTIONAL - Max upper birghtness/color diff; def: 20
		* fixedRng - OPTIONAL - TRUE=FIXED diff btw curr and see; FALSE=MASK only fills mask def:False
		* connectivity - OPTIONAL - 4 or 8 bit neightborrhood, def:8
	Returns:
		* Flood Filles Img
	"""
	flooded = img.copy()
	h, w = img.shape[:2]
	mask = np.zeros((h+2,w+2), np.uint8)
	flags = connectivity
	if fixedRng:
		flags |= cv2.FLOODFILL_FIXED_RANGE
	cv2.floodFill(flooded, mask, seedPoint, val, (lo,)*3, (hi,)*3, flags)
	return flooded




























