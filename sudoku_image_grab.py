import cv2 as cv
import numpy as np

img = cv.imread('sudoku.jpg', 0)


# Code to show image without proper resizing and close on key press
def display_image(image):
    cv.imshow('image', image)
    cv.waitKey(0) # waits at this point till key is pressed - can also allow time instead of 0
    cv.destroyAllWindows()


gray = cv.GaussianBlur(img, (5, 5), 0)
gray = cv.adaptiveThreshold(gray, 255, 1, 1, 11, 2)

