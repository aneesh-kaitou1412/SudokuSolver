import cv2
import numpy as np

img = cv2.imread(filename='sudoku.jpg', flags=0)


# Code to show image without proper resizing and close on key press
def display_image(image):
    cv2.imshow(winname='image', mat=image)
    cv2.waitKey(0)  # waits at this point till key is pressed - can also allow time instead of 0
    cv2.destroyAllWindows()


def point_order(arr):
    arr = np.reshape(a=arr, newshape=(4, 2))
    res = []
    res.append(arr[np.argmin(np.sum(a=arr, axis=1))])
    res.append(arr[np.argmin(np.diff(a=arr, axis=1))])
    res.append(arr[np.argmax(np.sum(a=arr, axis=1))])
    res.append(arr[np.argmax(np.diff(a=arr, axis=1))])
    res = np.asarray(res, dtype=np.float32)
    return res


gray = cv2.GaussianBlur(src=img, ksize=(5, 5), sigmaX=0)
gray = cv2.adaptiveThreshold(src=gray, maxValue=255, adaptiveMethod=1, thresholdType=1, blockSize=11, C=2)
img = cv2.imread(filename='sudoku.jpg')

img2, contours, hierarchy = cv2.findContours(image=gray, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
largest = None
area = 0
for c in contours:
    c_area = cv2.contourArea(contour=c)
    if c_area > 100:
        perimeter = cv2.arcLength(curve=c, closed=True)
        apprx_shape = cv2.approxPolyDP(curve=c, epsilon=0.02 * perimeter, closed=True)
        if len(apprx_shape) == 4 and c_area > area:
            area = c_area
            largest = apprx_shape

# cv2.drawContours(image=img, contours=largest, contourIdx=-1, color=(0, 255, 0), thickness=3)
# display_image(image=img)

ref = np.array([[0, 0], [449, 0], [449, 449], [0, 449]], np.float32)
largest = point_order(largest)
# print(largest)

# requires points to be np.float32 array of x y coordinates
affine_mat = cv2.getPerspectiveTransform(src=largest, dst=ref)
warped_img = cv2.warpPerspective(img, affine_mat, (450, 450))


