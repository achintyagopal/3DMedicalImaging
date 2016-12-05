import pickle
import Projection
import cv2
import numpy as np
import images


def projection_based_vector(points, faces, shape):
    
    img = Projection.project_mesh(points, faces, shape)

    # with open('img.file', 'wb') as writer:
    	# pickle.dump(img, writer)

    # with open('img.file', 'rb') as reader:
    	# img = pickle.load(reader)

    smoothed_img = Projection.smooth_projection(img)
    ellipses = Projection.gradient_descent(smoothed_img, iteration=100, win=10)

    right, left, nose = ellipses

    right_center_3d = get3d(right[0], img)
    if right[1][0] > right[1][1]:
    	right_maj_len = right[1][0]
    	right_min_len = right[1][1]
    else:
    	right_maj_len = right[1][1]
    	right_min_len = right[1][0]
    # right_maj_endpoint_1 = right_center_3d[0] + int(np.sin(right[2]) * .5 * right_maj_len), right_center_3d[1] + int(np.cos(right[2]) * .5 * right_maj_len)
    # right_maj_endpoint_2 = right_center_3d[0] - int(np.sin(right[2]) * .5 * right_maj_len), right_center_3d[1] - int(np.cos(right[2]) * .5 * right_maj_len)
    # right_min_endpoint_1 = right_center_3d[0] + int(np.cos(right[2]) * .5 * right_min_len), right_center_3d[1] + int(np.sin(right[2]) * .5 * right_min_len)
    # right_min_endpoint_2 = right_center_3d[0] - int(np.cos(right[2]) * .5 * right_min_len), right_center_3d[1] - int(np.sin(right[2]) * .5 * right_min_len)
    # right_maj_endpoints_3d = get3d(right_maj_endpoint_1, img), get3d(right_maj_endpoint_2, img)
    # right_min_endpoints_3d = get3d(right_min_endpoint_1, img), get3d(right_min_endpoint_2, img)

    left_center_3d = get3d(left[0], img)
    if left[1][0] > left[1][1]:
    	left_maj_len = left[1][0]
    	left_min_len = left[1][1]
    else:
    	left_maj_len = left[1][1]
    	left_min_len = left[1][0]
    # left_maj_endpoint_1 = left_center_3d[0] + int(np.sin(left[2]) * .5 * left_maj_len), left_center_3d[1] + int(np.cos(left[2]) * .5 * left_maj_len)
    # left_maj_endpoint_2 = left_center_3d[0] - int(np.sin(left[2]) * .5 * left_maj_len), left_center_3d[1] - int(np.cos(left[2]) * .5 * left_maj_len)
    # left_min_endpoint_1 = left_center_3d[0] + int(np.cos(left[2]) * .5 * left_min_len), left_center_3d[1] + int(np.sin(left[2]) * .5 * left_min_len)
    # left_min_endpoint_2 = left_center_3d[0] - int(np.cos(left[2]) * .5 * left_min_len), left_center_3d[1] - int(np.sin(left[2]) * .5 * left_min_len)
    # left_maj_endpoints_3d = get3d(left_maj_endpoint_1, img), get3d(left_maj_endpoint_2, img)
    # left_min_endpoints_3d = get3d(left_min_endpoint_1, img), get3d(left_min_endpoint_2, img)

    nose_center_3d = get3d(nose[0], img)
    if nose[1][0] > nose[1][1]:
    	nose_maj_len = nose[1][0]
    	nose_min_len = nose[1][1]
    else:
    	nose_maj_len = nose[1][1]
    	nose_min_len = nose[1][0]
    # nose_maj_endpoint_1 = nose_center_3d[0] + int(np.sin(nose[2]) * .5 * nose_maj_len), nose_center_3d[1] + int(np.cos(nose[2]) * .5 * nose_maj_len)
    # nose_maj_endpoint_2 = nose_center_3d[0] - int(np.sin(nose[2]) * .5 * nose_maj_len), nose_center_3d[1] - int(np.cos(nose[2]) * .5 * nose_maj_len)
    # nose_min_endpoint_1 = nose_center_3d[0] + int(np.cos(nose[2]) * .5 * nose_min_len), nose_center_3d[1] + int(np.sin(nose[2]) * .5 * nose_min_len)
    # nose_min_endpoint_2 = nose_center_3d[0] - int(np.cos(nose[2]) * .5 * nose_min_len), nose_center_3d[1] - int(np.sin(nose[2]) * .5 * nose_min_len)
    # nose_maj_endpoints_3d = get3d(nose_maj_endpoint_1, img), get3d(nose_maj_endpoint_2, img)
    # nose_min_endpoints_3d = get3d(nose_min_endpoint_1, img), get3d(nose_min_endpoint_2, img)

    features = []

    # roundedness of eyes and nose
    features.append(right_maj_len / right_min_len)
    features.append(left_maj_len / left_min_len)
    features.append(nose_maj_len / nose_min_len)

    # distance between eyes / horizontal offset of nose and eyes
    features.append(dist(right_center_3d, left_center_3d) / dist(tuple(np.subtract(right_center_3d, left_center_3d)), nose_center_3d))

    # distance between eyes / width of face
    features.append(dist(right_center_3d, left_center_3d) / get_face_width(right[0], left[0], img))

    # distance between right eye and nose / distance between left eye and nose
    right_to_nose_dist = dist(right_center_3d, nose_center_3d)
    left_to_nose_dist = dist(left_center_3d, nose_center_3d)
    features.append(right_to_nose_dist / left_to_nose_dist)

    # angle between vectors from eyes to nose
    normalized_vect_right = normalize(tuple(np.subtract(right_center_3d, nose_center_3d)), right_to_nose_dist)
    normalized_vect_left = normalize(tuple(np.subtract(left_center_3d, nose_center_3d)), left_to_nose_dist)
    features.append(angle_between(normalized_vect_right, normalized_vect_left))

    return np.array(features)


def normalize(tup, norm):
	a = []
	for i in xrange(3):
		a.append(tup[i] / norm)

	return (a[0], a[1], a[2])


def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    print v1
    print v2
    print ""
    return np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0))


def get_face_width(right_eye, left_eye, img):
	[vx,vy,x,y] = cv2.fitLine(np.array([right_eye, left_eye]),cv2.DIST_L2, 0, .01, .01)
	dy = float(vy) / float(vx)

	right_y = right_eye[0]
	right_x = right_eye[1]

	while img.item((int(right_x), int(right_y))) != 0:
		right_x += 1
		right_y -= dy

	left_y = left_eye[0]
	left_x = left_eye[1]
	while img.item((int(left_x), int(left_y))) != 0:
		left_x -= 1
		left_y += dy

	return dist((right_x, right_y), (left_x, left_y))


def dist(one, two):
	return np.linalg.norm(np.array(list(one)) - np.array(list(two)))


def get3d(center, img, window = (5,5)):
	x1, y1 = center

	ySize, xSize = img.shape[:2]
	w = window[0] / 2.0
	yL = int(max(0, y1 - w))
	xL = int(max(0, x1 - w))
	xR = int(min(xSize, x1 + w + 1))
	yR = int(min(ySize, y1 + w + 1))
	patch = img[yL:yR, xL:xR].copy() #Find Coord
	
	return (x1, y1, np.amax(patch))
