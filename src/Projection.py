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
			# py = math.log(2 * y - py + 1)
			py = 2 * y - py + 1
			pz *= 2

			val = img.item(pz, px)

			if val == 0:
				img.itemset((pz, px), py)
			elif val < py:
				img.itemset((pz, px), py)
	

	max_val = np.amax(img)
	img = img * float(255 / max_val)
	# print np.amin(img)
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
    # gray = grayscale(img)
    lap = cv2.Laplacian(img, cv2.CV_64F)
    return lap


def sobelx(img, ksize=5):
    """
    Applies a Sobel Kernel in the X Direction
    Derivative in X Dir
    """
    # gray = grayscale(img)
    sx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=ksize)
    return sx


def sobely(img, ksize=5):
    """
    Applies a Sobel Kernel in the Y Direction
    Derivative in Y Dir
    """
    # gray = grayscale(img)
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
	# not_img = cv2.bitwise_not(np.array(img * 255.0 / np.amax(img), dtype=np.uint8))
	max_y, max_x = img.shape


	# cv2.imshow("not", not_img)
	# dx = sobelx(not_img, 7)
	# dy = sobely(not_img, 7)
	# Nose
	
	parts = {}

	minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(img)
	# print maxLoc
	cv2.circle(color, maxLoc, 1, (255, 0, 255), 5)
	parts["Global_Max"] = maxLoc

	img = img.copy()
	img[img==0] = 65535
	
	win_center = win / 2

	start = (maxLoc[1], maxLoc[0]-20)
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
		# print "VALS:", minVal, minLoc
		local_min_x, local_min_y = minLoc
		new_y = local_min_y - win_center + start[0]
		new_x = local_min_x - win_center + start[1]
		cv2.line(color, (start[1], start[0]), (new_x, new_y), (255, 56, 45), 4)
		start = (new_y, new_x)
		# print start
		count += 1
		
		

	cv2.circle(color, (start[1], start[0]), 1, (255, 56, 45), 5)
	# print "END"
	
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
		# print "VALS:", minVal, minLoc
		local_min_x, local_min_y = minLoc
		new_y = local_min_y - win_center + start[0]
		new_x = local_min_x - win_center + start[1]
		cv2.line(color, (start[1], start[0]), (new_x, new_y), (100, 255, 60), 4)
		start = (new_y, new_x)
		# print start
		count += 1	
	
	cv2.circle(color, (start[1], start[0]), 1, (0, 255, 0), 5)
	# Chin:
	# chin_roi = img[maxLoc[1]+25:maxLoc[1]+80, maxLoc[0]-150:maxLoc[0]+150]
	# minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(chin_roi)
	# print maxLoc
	# maxLoc = (maxLoc[0] + , maxLoc[1] + 150)
	# maxLoc = (parts["Nose"][0] + maxLoc[0] + 25, parts[Nose][1] + maxLoc[1] + 150)
	# cv2.circle(color, maxLoc, 1, (0, 0, 255), 5)

	# cv2.imshow("chin", chin_roi)
	

	# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
	# dx = cv2.dilate(sobelx(not_img, 3), kernel, iterations = 2)
	# dy = cv2.dilate(sobely(not_img, 3), kernel, iterations = 2)

	# cv2.imshow("dx", np.array(abs(dx) * 255.0 / np.amax(abs(dx)), dtype=np.uint8))
	# cv2.imshow("dy", np.array(abs(dy) * 255.0 / np.amax(abs(dy)), dtype=np.uint8))

	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	"""
	a_x = 450
	a_y = 30

	for i in xrange(iteration):
		print a_x
		print a_y
		print gamma * dx.item(a_y, a_x)
		print gamma * dy.item(a_y, a_x)
		print "\n"
		b_x = a_x - gamma * dx.item(a_y, a_x)
		b_y = a_y - gamma * dy.item(a_y, a_x)
		if b_y < 0:
			b_y = 0
		elif b_y > max_y:
			b_y = max_y 
		if b_x < 0:
			b_x = 0
		elif b_x > max_x:
			b_x = max_x 
		cv2.line(color, (int(a_x), int(a_y)) , (int(b_x), int(b_y)) , (0, 255, 0), 2)
		a_x = b_x
		a_y = b_y


	# for i in xrange(len(next_guess)):
		# if i == len(next_guess) - 1:
	
			# break
	"""
	return color



	# color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
	# print np.amax(img)
	# ret, th = cv2.threshold(np.array(img * 255.0 / np.amax(img), dtype=np.uint8), 203, 255, cv2.THRESH_BINARY)
	# print ret

	# return th
	"""
	# lap = laplacian(img)
	# Start
	a_x = 380
	a_y = 23

	for i in xrange(0, iterations):
		print (a_x, a_y)
		fx_win = getWindow(fx, (a_y, a_x), window=(15,15))
		fy_win = getWindow(fy, (a_y, a_x), window=(15,15))
		print np.mean(fx_win)
		print np.mean(fy_win)

		if min_val:
			b_x = int( a_x + gamma * np.mean(fx_win) )
			b_y = int( a_y + gamma * np.mean(fy_win) )
			cv2.line(color, (a_x, a_y), (b_x, b_y), (0, 255, 0), 2)
			a_x = b_x
			a_y = b_y
			print (b_x, b_y)
			print "\n"
		else: 
			b_x = int( a_x - gamma * np.mean(fx_win) )
			b_y = max(int( a_y - gamma * np.mean(fy_win) ), 0 )
			cv2.line(color, (a_x, a_y), (b_x, b_y), (0, 255, 0), 2)
			a_x = b_x
			a_y = b_y
			print (b_x, b_y)
			print "\n"
	return color
	"""







