import cv2
import numpy as np
import matplotlib.pyplot as plt 
import argparse
# import os
# import pytesseract
# from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument('--images', type=str, nargs='+')

args = parser.parse_args()

for image_path in args.images:
	image = cv2.imread(image_path)
	gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	## Denoising and Adaptive Thresholding
	denoised_image = cv2.fastNlMeansDenoising(gray_image)
	denoised_adapted_image = cv2.adaptiveThreshold(denoised_image, 255, 
												cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
												cv2.THRESH_BINARY, 
												11, 2)

	## Canny Edge Detection and Finding all Maximal Boundaries
	edges = cv2.Canny(denoised_adapted_image, 100, 255)
	# mask = edges != 0
	# canny_image = denoised_adapted_image * (mask[:,:].astype(denoised_adapted_image.dtype))
	contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	
	## Finding the Largest Area Contour
	max_area = 0
	max_area_contour = None
	for contour in contours:
		if cv2.contourArea(contour) > max_area:
			max_area = cv2.contourArea(contour)
			max_area_contour = contour
	# cv2.drawContours(gray_image, max_area_contour, -1, (0, 255, 0), 3)
	
	## Finding the corners of the sudoku
	rectangle = cv2.approxPolyDP(max_area_contour, 20, True)
	# cv2.drawContours(gray_image, rectangle, -1, (0, 255, 0), 3)
	
	## Sorting the boundary points
	rectangle = rectangle[np.argsort(rectangle[:,0,0])]
	rectangle[:2,:,:] = rectangle[:2,:,:][np.argsort(rectangle[:2,:,:][:,0,1])]
	rectangle[2:,:,:] = rectangle[2:,:,:][np.argsort(rectangle[2:,:,:][:,0,1])]
	rectangle = np.asarray([r[0] for r in rectangle], dtype=np.float32)

	## Getting image boundaries
	image_shape = []
	for x in [0, gray_image.shape[0]-1]:
		for y in [0, gray_image.shape[1]-1]:
			image_shape.append([x, y])
	image_shape = np.asarray(image_shape, dtype=rectangle.dtype)

	# print(rectangle)
	# print(image_shape)

	## Perspective Transform
	transformer = cv2.getPerspectiveTransform(rectangle, image_shape)
	warped_image = cv2.warpPerspective(denoised_adapted_image, transformer, gray_image.shape)

	## Find the grid lines
	contours, hierarchy = cv2.findContours(warped_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	color_warped_image = cv2.cvtColor(warped_image, cv2.COLOR_GRAY2RGB)
	cv2.drawContours(color_warped_image, contours, -1, (255, 255, 0), hierarchy=hierarchy)

	## Display and Wait
	cv2.imshow('Original image', image)
	cv2.imshow('Contours on image', color_warped_image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	# cv2.imwrite("temp.png", warped_image)

	# text = pytesseract.image_to_string(Image.open("temp.png"))
	# os.remove("temp.png")
	# print(text)