# 3DMedicalImaging

Run "python main.py <data_file.nii>"

For development purpose, intermediary is saved in testData/.

Structure

src/
	2Dlabelling/
	3Dlabelling/
	corners/
	meshing/
	threshold/
	
	2DlabellingTest.py
	3DlabellingTest.py
	cornersTest.py
	labellingTest.py
	meshingTest.py
	thresholdTest.py
testData/
	
main.py
README.md

Input:
	threshold : <data_file>.nii.gz
	2Dlabelling : <data_file>_threshold.nii.gz
	3Dlabelling : <data_file>_2dlabelling.nii.gz
	corners : <data_file>_3dlabelling.nii.gz
	meshing : <data_file>_corners.nii.gz

Output
	meshing (and main) : <data_file>.mesh