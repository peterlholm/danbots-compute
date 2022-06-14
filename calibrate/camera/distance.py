import cv2
import numpy as np
from compute.settings import BASE_DIR

_DEBUG = True

imagefile = BASE_DIR / 'calibrate/camera/testimages/dist/picture5.jpeg'

def calc_dist(imagefile):
    img = cv2.imread(str(imagefile))
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    if _DEBUG:
        cv2.imshow('color', img)
        cv2.imshow('grey', gray_img)

    cnts = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for cnt in cnts:
        approx = cv2.contourArea(cnt)
        print(approx)
    if _DEBUG:
        print("HER")
        cv2.imshow('image', img)
    cv2.imshow('Binary',thresh_img)
    cv2.waitKey()
    return 7
