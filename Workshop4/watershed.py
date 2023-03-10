import imutils
import cv2 as cv
import numpy as np

class Watershed(object):
    def __init__(self, img, threshold, maxval) -> None:
        self.img = img
        self.threshold = threshold
        self.maval = maxval

        self.img_gray = None
        self.img_threshold = None

    def gray_scale(self):
        self.img_gray = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)

    def threshold_binary(self):
        self.img_threshold = cv.threshold(self.img_gray, self.threshold, self.maval,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)[1]

    def draw_boder(self):
        kernel = np.ones((3,3),np.uint8)
        opening = cv.morphologyEx(self.img_threshold, cv.MORPH_OPEN,kernel, iterations = 2)

        sure_bg = cv.dilate(opening,kernel,iterations=3)

        dist_transform = cv.distanceTransform(opening,cv.DIST_L2,5)

        _, sure_fg = cv.threshold(dist_transform,0.7*dist_transform.max(),255,0)

        sure_fg = np.uint8(sure_fg)

        unknown = cv.subtract(sure_bg,sure_fg)

        _, markers = cv.connectedComponents(sure_fg)

        markers = markers+1

        markers[unknown==255] = 0

        markers = cv.watershed(self.img,markers)

        self.img[markers == -1] = [255, 0, 0]


  
    

#test;
path_img = None
img = cv.imread(path_img)
watershed = Watershed(img, 0, 255)
watershed.gray_scale()
watershed.threshold_binary()
watershed.draw_boder()

cv.imshow("test", watershed.img)
cv.waitKey(0)
