#Paul
import os

src_path = './'
dst_path = '../good/'
num_files = 113

for i in xrange(0, num_files):
	src = src_path + str(i).zfill(6) + ".dcm"

	j = num_files - i - 1
	dst = dst_path + str(j).zfill(6) + ".dcm"

	#print src, dst
	os.rename(src, dst)
