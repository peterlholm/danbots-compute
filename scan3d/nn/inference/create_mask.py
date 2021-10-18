"Create the mask file"
from pathlib import Path
import numpy as np
import cv2
from .config import PICTURE_HEIGHT, PICTURE_WIDTH, MASK_NPY, MASK_FILENAME

_DEBUG=False

def make_grayscale(img):
    # Transform color image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray_img

def create_mask(color_picture, nolight_picture, outfolder):
    if _DEBUG:
        print("creating mask")
    outfolder = Path(outfolder)
    #color = folder / 'image8.png'
    #print('color:', color_picture)
    img1 = np.zeros((PICTURE_HEIGHT, PICTURE_WIDTH), dtype=np.float)
    img1 = cv2.imread(str(color_picture), 1).astype(np.float32)
    gray = make_grayscale(img1)
    #black = folder / 'image9.png'
    img2 = np.zeros((PICTURE_HEIGHT, PICTURE_WIDTH), dtype=np.float)
    img2 = cv2.imread(str(nolight_picture), 0).astype(np.float32)
    diff1 = np.subtract(gray, .5*img2)
    my_mask =  np.zeros((PICTURE_HEIGHT, PICTURE_WIDTH), dtype=np.float)
    for i in range(PICTURE_HEIGHT):
        for j in range(PICTURE_WIDTH):
            if (diff1[i,j]<50):
                my_mask[i,j]= True
    np.save( Path(outfolder) / MASK_NPY, my_mask, allow_pickle=False)
    cv2.imwrite( str(outfolder / MASK_FILENAME), 128*my_mask)
    return my_mask
