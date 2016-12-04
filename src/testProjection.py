import cv2
import numpy as np 
import Projection
import pickle
import HaarDetection

"""
project_mesh
smooth_projection
gradient_descent
laplacian
"""

def test(points, faces, ker=4, scale=700):

	# print "Start"
	# img = Projection.project_mesh(points, faces, shape)
	# print "Finish"

	# tmp = Projection.smooth_projection(img)
	tmp = cv2.imread("projection.jpg", 0)
		
	# lap = Projection.laplacian(tmp)
	lap = cv2.imread("lap.jpg", 0)
	# cv2.imwrite("lap.jpg", np.array(lap * 255.0 / np.amax(lap), dtype=np.uint8))
	# x = Projection.sobelx(cv2.bitwise_not(tmp), 3)
	# y = Projection.sobely(cv2.bitwise_not(tmp), 3)

	# cv2.namedWindow("pic", cv2.WINDOW_NORMAL)
	# cv2.imshow("pic", tmp)

	cv2.namedWindow("lap", cv2.WINDOW_NORMAL)
	cv2.imshow("lap", lap)
	# cv2.imwrite("tmp.jpg", np.array(tmp)

	gd = Projection.gradient_descent(tmp, iteration=100, win=10)
	cv2.namedWindow("gd", cv2.WINDOW_NORMAL)
	cv2.imshow("gd", gd)
	
	cv2.imwrite("grad_des_ret.jpg", gd)

	# cv2.namedWindow("x", cv2.WINDOW_NORMAL)
	# cv2.imshow("x", np.array(abs(x), dtype=np.uint8))

	# cv2.namedWindow("y", cv2.WINDOW_NORMAL)
	# cv2.imshow("y", np.array(abs(y), dtype=np.uint8))

	# cv2.imwrite("bin.jpg", gd)
	# cv2.imwrite("projection.jpg", tmp * 255.0 / np.amax(tmp))
	# cv2.namedWindow("haar", cv2.WINDOW_NORMAL)
	# cv2.imshow("haar", fa)

	cv2.waitKey(0)
	cv2.destroyAllWindows()




# shape = [98, 512, 512]
# with open("faces.file", 'rb') as reader:
	# faces = pickle.load(reader)


# with open("points.file", 'rb') as reader:
	# points = pickle.load(reader)
# for i in xrange(1, 10):
points = []
faces = []
test(points, faces)


