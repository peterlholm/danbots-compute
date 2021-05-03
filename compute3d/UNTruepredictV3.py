import numpy as np
import os
import cv2
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import math
import os.path
from os import path
import tensorflow as tf
# add to the top of your code under import tensorflow as tf
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)
import tensorflow.keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras import optimizers
from tensorflow.python.keras.layers import Layer, InputSpec
# from tensorflow.keras.engine.topology import Layer
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, BatchNormalization, Lambda, Input
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Add, UpSampling2D, concatenate, Concatenate, AveragePooling2D
from tensorflow.keras.utils import plot_model
import time
# import nnwrap as nnw
import argparse
import sys
# import myglobals

from compute.settings import DATA_PATH

#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

MODEL_PATH = DATA_PATH / 'nnmodels/'
#H_MODELFILE = 'UN30-400-WUN-100-V2.h5'
H_MODELFILE = 'UN15-680-mat-b8-Wrap-100-V2.h5'

PI = np.pi



high_freq = 14 #14
low_freq = .705
rwidth = 160
rheight = 160
H =160
W = 160

def resize(img, w,h):
    print(img.shape)
    img = img[0:160,0:160]
    print( img.shape )
    return(img)




def make_grayscale(img):
    # Transform color image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray_img


def normalize_image255(img):
    # Changes the input image range from (0, 255) to (0, 1)number_of_epochs = 5
    img = img/255.0
    return img


def normalize_image(img):
    # Normalizes the input image to range (0, 1) for visualization
    img = img - np.min(img)
    img = img/np.max(img)
    return img



def load_H_model():
    # model = tensorflow.keras.models.load_model('/home/samir/dblive/cnnpredict/models/UNmodels/UNet02-224-fringe-wrapdata'+'-200-adam-noBN.h5')
    print ("Path", MODEL_PATH / H_MODELFILE)
    model = tensorflow.keras.models.load_model(MODEL_PATH / H_MODELFILE)

    return(model)
# /home/samir/dblive/cnnpredict/models/cnnres01-220-modelwrap1'+'-200-adam-noBN.h5

def load_L_model():
    model = tensorflow.keras.models.load_model(MODEL_PATH + 'UN30-UNW-800TF-120.h5')
    return(model)

def makemonohigh(folder):
    high = folder + 'high.png'
    colorhigh = cv2.imread(high, 1)
    monohigh = make_grayscale(colorhigh)
    cv2.imwrite(folder+'monohigh.png', monohigh)
    return


def mask(folder):
    color = folder / 'image8.png'
    print('color:', color)
    img1 = np.zeros((H, W), dtype=np.float)
    img1 = cv2.imread(str(color), 1).astype(np.float32)
    gray = make_grayscale(img1)


    black = folder / 'image9.png'
    img2 = np.zeros((H, W), dtype=np.float)
    img2 = cv2.imread(str(black), 0).astype(np.float32)
    diff1 = np.subtract(gray, .5*img2)
    mask =  np.zeros((H, W), dtype=np.float)
    for i in range(H):
        for j in range(W):
            if (diff1[i,j]<50):
                mask[i,j]= True
    np.save( folder / 'mask.npy', mask, allow_pickle=False)
    cv2.imwrite( str(folder / 'mask.png'), 128*mask)
    return(mask)


def DB_predict( model, x):
    predicted_img = model.predict(np.array([np.expand_dims(x, -1)]))
    predicted_img = predicted_img.squeeze()
    # tensorflow.keras.backend.clear_session()
    return(predicted_img)




def nnHprocess(folder):
    high = folder / 'image0.png' #'blenderimage0.png' or 'image0.png'
    image1 = cv2.imread(str(high), 1).astype(np.float32)
    # black = folder + 'image9.png' #'' blenderblack.png or 'image9.png'
    # image2 = cv2.imread(black,1).astype(np.float32)
    image = image1 #- image2
    inp_1 = normalize_image255(image)
    inp_1 = make_grayscale(inp_1)
    # mask = np.load(folder+'mask.npy')
    # inp_1 = np.multiply(np.logical_not(mask), inp_1)
    # Hmodel = load_H_model()

    start = time.time()
    predicted_img = DB_predict(Hmodel, inp_1)
    end = time.time()
    print('elapsed high:', end-start)

    # mask = np.load(folder+'mask.npy')
    # wrapH = np.multiply(np.logical_not(mask), predicted_img)
    # wrapH = resize(wrapH, W, H)
    np.save(folder / 'unwrap1.npy', predicted_img, allow_pickle=False)
    cv2.imwrite( str(folder / 'unwrap1.png'),255*predicted_img)
    return  #(predicted_img[0], predicted_img[1])

def nnLprocess(folder):
    high = folder + 'unwrap1.png'
    image = cv2.imread(high, 1).astype(np.float32)
    inp_1 = normalize_image255(image)
    inp_1 = make_grayscale(inp_1)
    # mask = np.load(folder+'mask.npy')
    # inp_1 = np.multiply(np.logical_not(mask), inp_1)
    # Hmodel = load_H_model()

    start = time.time()
    predicted_img = DB_predict(Lmodel, inp_1)
    end = time.time()
    print('elapsed low:', end-start)

    mask = np.load(folder+'mask.npy')
    unwdata = predicted_img # mask is not calculated properly
    # unwdata = np.multiply(np.logical_not(mask), predicted_img)
    # kdatay = 255/6*predicted_img
    # kdatay = np.round(kdatay)
    # print('kdatay:', kdatay[::40, ::40])
    np.save(folder + 'nnunwrap.npy', 80*unwdata, allow_pickle=False)
    # prdicted_img = np.round(predicted_img*17/(np.max(predicted_img)))
    cv2.imwrite( folder + 'nnunwrap.png',255*unwdata)
    # print('255*kdata:', 255*kdata[::40, ::40])


    return  #(predicted_img[0], predicted_img[1])



def unwrap_k(folder):
    kdata = np.zeros((H, W), dtype=np.float64)
    wraphigh = np.zeros((H, W), dtype=np.float64)
    unwrapdata = np.zeros((H, W), dtype=np.float64)
    kdata = np.load(folder + '/nnkdata.npy')  # Use a factor of 37.5 when using nnkdata!

    kdata = np.round(37.5*kdata)  # Use a factor of 37.5 when using nnkdata!
    # kdata = np.round(kdata/4)
    # kdata = kdata*4
    # kdata = np.matrix.round(45*kdata)

    # wraplow = resize(wraplow, W, H)  # To be continued
    wraphigh = (np.load(folder + '/unwrap1.npy'))
    wraphigh = wraphigh - np.min(wraphigh)
    wraphigh = wraphigh/ np.max(wraphigh)
    wraphigh = wraphigh*2*PI
    print('highrange=', np.ptp(wraphigh), np.max(wraphigh), np.min(wraphigh) )
    print('nnkdatarange=', np.ptp(kdata), np.max(kdata), np.min(kdata) )
    # wraphigh = normalize_image(wraphigh)
    # wraphigh = 2*PI*wraphigh
    # print('highrange=', np.ptp(wraphigh), np.max(wraphigh), np.min(wraphigh) )
    unwrapdata = np.add(wraphigh, np.multiply(2*PI,kdata) )
    print('kdata:', kdata[::40, ::40])
    print('nnunwrange=', np.ptp(unwrapdata), np.max(unwrapdata), np.min(unwrapdata) )
    wr_save = folder + '/nnkunwrap.npy'
    np.save(wr_save, unwrapdata, allow_pickle=False)
    cv2.imwrite(folder + '/nnkunwrap.png', 3.0*unwrapdata)




def makeDDbase(count):
    print('start')
    phibase = np.zeros((H, W,count), dtype=np.float64)
    for u in range(W):
        for v in range(H):
            print('u=', u, 'v=', v)
            for i in range(count):
                # print('i=',i)
                folder = '/home/samir/Desktop/blender/pycode/160scanplanes/render'+ str(i)+'/'
                unwrap = np.zeros((H, W), dtype=np.float64)
                unwrap = np.load(folder+'unwrap.npy')   
                phibase[u,v,i] = unwrap[u,v]
    folder = '/home/samir/Desktop/blender/pycode/160scanplanes/'
    wr_save = folder + 'DDbase.npy'
    np.save(wr_save, phibase, allow_pickle=False)


def makeDepth( folder, basecount):
    basefile = '/home/samir/Desktop/blender/pycode/300numplanes/DDbase.npy'
    DBase = np.load(basefile)
    unwrap = np.load(folder+'/nnkunwrap.npy' )
    # print('DBase:', np.amax(DBase), np.amin(DBase))
    # print('unwrap:', np.amax(unwrap), np.amin(unwrap))
    depth = np.zeros((H, W), dtype=np.float64)
    for i in range(W):
        # print('i:', i)
        for j in range(H):
            s=0
            for s in range(basecount-1):
                if (abs(unwrap[i,j]-DBase[i,j,s])<.15):
                    break
                else:
                    s+=1

            # print(i,j,unwrap[i,j],DBase[i,j,s])
            depth[i,j]=s
            # print('found:',i,j, unwrap[i,j], DBase[i,j,s],s)
    
    # print('depth:', np.amax(depth), np.amin(depth))
    # print(depth)
    im_depth = depth# np.max(unwrapdata)*255)
    cv2.imwrite(folder + '/nndepth.png', im_depth)

def newDepth(folder, basecount):
    basefile = '/home/samir/Desktop/blender/pycode/15depthplanes/DDbase.npy'
    DBase = np.load(basefile)
    unwrap = np.load(folder+'/nnunwrap.npy' )
    mask = np.load(folder+'/mask.npy' )
    # print('DBase:', np.amax(DBase), np.amin(DBase))
    # print('unwrap:', np.amax(unwrap), np.amin(unwrap))
    depth = np.zeros((rheight, rwidth), dtype=np.float64)
    zee=0
    for i in range(rwidth):
        # print('i:', i)
        for j in range(rheight):
            if not(mask[i,j]):

                s=0
                for s in range(0, basecount-1,10):
                    if (unwrap[i,j]< DBase[i,j,s]):
                        ds = (unwrap[i,j] - DBase[i,j,s])/( DBase[i,j,s]- DBase[i,j,s-10])
                        zee = s+ds*10
                        break
                    else:
                        s+=1
                        if s==250:
                            print('not found!')

                # print(i,j,unwrap[i,j],DBase[i,j,s])
                if zee == 0:
                    print('not found')
                depth[i,j]= (zee/250*-25 + 40)*1

    # print('depth:', np.amax(depth), np.amin(depth))
    print('nndepthrange=', np.ptp(depth), np.max(depth), np.min(depth) )

    im_depth = depth# np.max(unwrapdata)*255)
    cv2.imwrite(folder + '/nndepth.png', im_depth)
    np.save(folder+'/nndepth.npy' ,im_depth , allow_pickle=False)




def nngenerate_pointcloud(rgb_file, mask_file,depth_file,ply_file):
    """
    Generate a colored point cloud in PLY format from a color and a depth image.
    
    Input:
    rgb_file -- filename of color image
    depth_file -- filename of depth image
    ply_file -- filename of ply file
    
    """
    rgb = Image.open(rgb_file)
    # depth = Image.open(depth_file)
    # depth = Image.open(depth_file).convert('I')
    depth = np.load(depth_file )
    mask = Image.open(mask_file).convert('I')

    # if rgb.size != depth.size:
    #     raise Exception("Color and depth image do not have  same resolution.")
    # if rgb.mode != "RGB":
    #     raise Exception("Color image is not in RGB format")
    # if depth.mode != "I":
    #     raise Exception("Depth image is not in intensity format")


    points = []    
    for v in range(rgb.size[1]):
        for u in range(rgb.size[0]):

            color =   rgb.getpixel((v,u))
            # Z = depth.getpixel((u,v)) / scalingFactor
            # if Z==0: continue
            # X = (u - centerX) * Z / focalLength
            # Y = (v - centerY) * Z / focalLength
            if (mask.getpixel((v,u))<55):
                # Z = depth.getpixel((u, v))
                Z = depth[u,v]
                if Z < 0:
                    Z = 0 
                else:
                    if Z> 80:
                        Z = 80
                if Z == 0: continue
                Y = .196 * (v-80) *  Z/80 #.196 = tan(FOV/2)
                X = .196 * (u-80) *  Z/80
                if (u==80 and v ==80):
                    print('80:z=', Z, X, Y)
                else:
                   if (u==102 and v ==82):
                        print('82:z=', Z, X, Y) 
                points.append("%f %f %f %d %d %d 0\n"%(X,Y,Z,color[0],color[1],color[2]))
    file = open(ply_file,"w")
    file.write('''ply
format ascii 1.0
element vertex %d
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
property uchar alpha
end_header
%s
'''%(len(points),"".join(points)))
    file.close()



def generate_pointcloud(rgb_file, mask_file,depth_file,ply_file):
    """
    Generate a colored point cloud in PLY format from a color and a depth image.
    
    Input:
    rgb_file -- filename of color image
    depth_file -- filename of depth image
    ply_file -- filename of ply file
    
    """
    print(rgb_file)
    rgb = Image.open(rgb_file)
    # depth = Image.open(depth_file)
    # depth = Image.open(depth_file).convert('I')
    depth = np.load(depth_file)
    mask = Image.open(mask_file).convert('I')

    # if rgb.size != depth.size:
    #     raise Exception("Color and depth image do not have the same resolution.")
    # if rgb.mode != "RGB":
    #     raise Exception("Color image is not in RGB format")
    # if depth.mode != "I":
    #     raise Exception("Depth image is not in intensity format")


    points = []    
    for v in range(rgb.size[1]):
        for u in range(rgb.size[0]):
            color =   rgb.getpixel((u,v))
            # Z = depth.getpixel((u,v)) / scalingFactor
            # if Z==0: continue
            # X = (u - centerX) * Z / focalLength
            # Y = (v - centerY) * Z / focalLength
            if (mask.getpixel((u,v))<55):
                Z = depth.getpixel((u, v))*.22 
                if Z == 0: continue
                Y = .22 * v
                X = .22 * u
                points.append("%f %f %f %d %d %d 0\n"%(X,Y,Z,color[0],color[1],color[2]))
    file = open(ply_file,"w")
    file.write('''ply
format ascii 1.0
element vertex %d
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
property uchar alpha
end_header
%s
'''%(len(points),"".join(points)))
    file.close()





def depth(scanfolder, count, basecount):
    for i in range(count):
        print('progress:', str(i))
        folder = '/home/samir/Desktop/blender/pycode/'+scanfolder+'/render'+ str(i)+'/'
        newDepth(folder, basecount)


def nndepth(scanfolder, count, basecount):
    for i in range(count):
        print('progress:', str(i))
        folder = '/home/samir/Desktop/blender/pycode/'+scanfolder+'/'+ str(i)+'/'
        makeDepth(folder, basecount)



def makeclouds(scanfolder, count):
     for i in range(count):
        print('start')
        folder = '/home/samir/Desktop/blender/pycode/'+scanfolder+'/render'+ str(i)+'/'
        print(folder)
        if path.exists(folder):
            # generate_pointcloud(folder + 'blendertexture.png', folder + '5mask.png' , folder + 'im_wrap1.png', folder +'pointcl-high.ply')
            # generate_pointcloud(folder + 'blendertexture.png', folder + '-1mask.png' , folder + 'im_wrap2.png', folder +'pointcl-low.ply')
            # generate_pointcloud(folder + 'blendertexture.png', folder + '-1mask.png', folder + 'nnkunwrap.png', folder +'pointcl-unw.ply')
            generate_pointcloud(folder + 'image9.png', folder + 'mask.png', folder + 'nndepth.png', folder +'pointcl-nndepth.ply')



####################################################################################################################

Hmodel = load_H_model()

def nnprocess_input(folder):
    #Lmodel = load_L_model()
    Hmodel = load_H_model()

  
    mask(folder)
    nnHprocess(folder)
    return
    nnLprocess(folder)
    newDepth(folder, 200)
    nngenerate_pointcloud(folder+'/'+ 'image8.png', folder+'/'+ 'mask.png', folder+'/' + 'nndepth.npy', folder+'/' +'pointcl-nndepth.ply')


# folder = '/home/samir/Desktop/blender/pycode/inputscans/render'
# bfolder = '/home/samir/Desktop/blender/pycode/inputscans/'


# Lmodel = load_L_model()
# Hmodel = load_H_model()

# for i in range(len(os.listdir(bfolder))-1):
    # folder = '/home/samir/Desktop/blender/pycode/inputscans/render'
    # folder = '/home/samir/db3/scan/static/scan_folder/scan_im_folder'

    # print('i:', i)
    # mask(folder+str(i)+'/')
    # unwrap_k(folder + str(i)+'/')
    # makemonohigh(folder+'i')

    # nnHprocess(folder + str(i)+'/')
    # nnLprocess(folder + str(i)+'/')
    # unwrap_k(folder + str(i)+'/')
    # newDepth(folder+ str(i)+'/' , 200)
    # nngenerate_pointcloud(folder+str(i) +'/'+ 'image8.png', folder+str(i) +'/'+ 'mask.png', folder+str(i)+'/' + 'nndepth.npy', folder+str(i)+'/' +'pointcl-nndepth.ply')

    # repairK(folder + str(i)+'/'+'unwrap1.png', folder + str(i)+'/'+'nnkdata.png', folder + str(i)+'/'+'krepdata.png' )

    # generate_pointcloud(folder + 'blendertexture.png', folder + 'mask.png', folder + 'unwrap.png', folder +'pointcl-unw.ply')

    # unw('scans', 44)
    # depth('scans', 44, 400)
    # makeclouds('scans', 44)
    # print('done!')





#========================================================= Parking Lot============================================================
