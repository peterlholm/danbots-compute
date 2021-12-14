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
    "Create a numpy array with 0: included, 1: excluded"
    if _DEBUG:
        print("creating mask", color_picture, nolight_picture)
    outfolder = Path(outfolder)
    #img1 = np.zeros((PICTURE_HEIGHT, PICTURE_WIDTH), dtype=np.float)
    #img1 = cv2.imread(str(color_picture), 1).astype(np.float32)
    img1 = cv2.imread(str(color_picture), -1).astype(np.float32)
    # first init mask with alfa channel if exist
    gray = make_grayscale(img1)
    if _DEBUG:
        cv2.imwrite(str(outfolder / 'grey.png'), gray)
        #print(gray)
    #black = folder / 'image9.png'
    img2 = np.zeros((PICTURE_HEIGHT, PICTURE_WIDTH), dtype=np.float)
    img2 = cv2.imread(str(nolight_picture), 0).astype(np.float32)
    diff1 = np.subtract(gray, .5*img2)
    my_mask =  np.zeros((PICTURE_HEIGHT, PICTURE_WIDTH), dtype=np.float)
    #cv2.imwrite( str(outfolder / 'test2.png'), 128*my_mask)
    for i in range(PICTURE_HEIGHT):
        for j in range(PICTURE_WIDTH):
            if (diff1[i,j]<50):
                my_mask[i,j]= True
    # if alfa channel

    if False and img1.shape[2]>3:
        channels = cv2.split(img1)
        # add alfa mask
        for i in range(img1.shape[0]):
            for j in range(img1.shape[1]):
                if channels[3][i][j]==0:
                    my_mask[i,j] = 1
    np.save( Path(outfolder) / MASK_NPY, my_mask, allow_pickle=False)
    #print(my_mask)
    cv2.imwrite( str(outfolder / MASK_FILENAME), 128*my_mask)
    return my_mask

def create_picture_mask(color_picture, nolight_picture, outfolder):
    "Create a numpy array with 0: included, 1: excluded"
    if _DEBUG:
        print("creating mask", color_picture, nolight_picture)
    outfolder = Path(outfolder)
    img1 = cv2.imread(str(color_picture), 1).astype(np.float32)
    #img1 = cv2.imread(str(color_picture), 1)-.astype(np.float32)
    gray = make_grayscale(img1)
    if _DEBUG:
        cv2.imwrite(str(outfolder / 'grey.png'), gray)
        #print(gray)
    img2 = np.zeros((PICTURE_HEIGHT, PICTURE_WIDTH), dtype=np.float)
    img2 = cv2.imread(str(nolight_picture), 0).astype(np.float32)
    diff1 = np.subtract(gray, .5*img2)
    my_mask =  np.zeros((PICTURE_HEIGHT, PICTURE_WIDTH), dtype=np.float)
    #cv2.imwrite( str(outfolder / 'test2.png'), 128*my_mask)
    for i in range(PICTURE_HEIGHT):
        for j in range(PICTURE_WIDTH):
            if (diff1[i,j]<50):
                my_mask[i,j]= True
    # if alfa channel

    np.save( Path(outfolder) / MASK_NPY, my_mask, allow_pickle=False)
    #print(my_mask)
    cv2.imwrite( str(outfolder / MASK_FILENAME), 128*my_mask)
    return my_mask

def create_0mask(color_picture, nolight_picture, outfolder):
    "Create a numpy array with 0: excluded, 1: included from included alfa channels"
    if _DEBUG:
        print("creating 0-mask", color_picture, nolight_picture)
    outfolder = Path(outfolder)
    img1 = cv2.imread(str(color_picture), -1).astype(np.int)
    # if alfa channel
    my_mask =  np.full((img1.shape[0], img1.shape[1]), 255, dtype=np.int)
    if img1.shape[2]>3:
        channels = cv2.split(img1)
        # add alfa mask
        for i in range(img1.shape[0]):
            for j in range(img1.shape[1]):
                if channels[3][i][j]==0:
                    my_mask[i,j] = 0
    np.save( Path(outfolder) / 'mask0.npy', my_mask, allow_pickle=False)
    if _DEBUG:
        cv2.imwrite( str(outfolder / 'mask0.png'), my_mask)
    return my_mask

def create_nomask(outfolder):
    my_mask =  np.zeros((PICTURE_HEIGHT, PICTURE_WIDTH), dtype=np.float)
    # for i in range(PICTURE_HEIGHT):
    #     for j in range(PICTURE_WIDTH):
    #         my_mask[i,j]= True
    #print(my_mask)
    np.save( Path(outfolder) / MASK_NPY, my_mask, allow_pickle=False)
    cv2.imwrite( str(outfolder / MASK_FILENAME), 128*my_mask)
    return my_mask
