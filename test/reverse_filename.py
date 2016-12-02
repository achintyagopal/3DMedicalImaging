#Paul
import os


src_path = './'
dst_path = '../good/'
num_files = 98

for i in xrange(0, num_files):
	if i < 10:
		src = src_path + '00000' + str(i) + '.dcm'
	elif i < 100:
		src = src_path + '0000' + str(i) + '.dcm'
	else:
		src = src_path + '000' + str(i) + '.dcm'

	j = num_files - i - 1
	if j < 10:
		dst = dst_path + '00000' + str(j) + '.dcm'
	elif j < 100:
		dst = dst_path + '0000' + str(j) + '.dcm'
	else:
		dst = dst_path + '000' + str(j) + '.dcm'

	os.rename(src, dst)