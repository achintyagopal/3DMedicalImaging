import numpy as np
import cv2

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
			py *= 2
			pz *= 2

			val = img.item(pz, px)

			if val == 0:
				img.itemset((pz, px), py)
			elif val < py:
				img.itemset((pz, px), py)
	max_val = np.amax(img)
	img = img * 255 / max_val
	return img




"""
TO DO:
* find features?
* find keypoints?

"""