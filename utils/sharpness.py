import cv2 as cv
import numpy as np


picture1 = 'testdata/device/serie1/input/1/color.jpg'
picture2 = 'testdata/device/serie1/input/1/color.jpg'
picture1 = 'testdata/wand/Beige_Toothset/piZ2_210907/1/color.jpg'
picture2 = 'testdata/wand/Beige_Toothset/piZ2_210907/2/color.jpg'


def variance_of_laplacian(image):
	# compute the Laplacian of the image and then return the focus
	# measure, which is simply the variance of the Laplacian
	return cv.Laplacian(image, cv.CV_64F).var()

def calc_sharpnes(img):
    a = variance_of_laplacian(img)
    print (a)

def gen_sharpness_picture(img):
    cv.imshow("img", img)
    h,  w = img.shape[:2]
    n = 4
    hp = h//n
    wp = w//n
    print(h,w, hp, wp)
    res = np.empty((n,n))
    nn = 0
    for x in range(n):
        for y in range(n):  
            print ("x", x*wp, "y", y*hp)  
            iarr = img[x*wp:wp, y*hp:hp]
            print(iarr)
            cv.imshow("uu"+str(nn),iarr )
            cv.waitKey(3000)
            nn += 1
im1 = cv.imread(picture1)
#calc_sharpnes(im1)
im2 = cv.imread(picture2)
#calc_sharpnes(im2)
res = gen_sharpness_picture(im2)
#cv.imshow("res", res)

