
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
import shutil
# import myglobals






PI = np.pi



high_freq = 14 #14
low_freq = .75
rwidth = 160
rheight = 160
H =160
W = 160

def resize(img, w,h):
    print(img.shape)
    img = img[0:160,0:160]
    print( img.shape )
    return(img)

def getnnplys(infolder ):       
    count=len(os.listdir(infolder))-3
    for i in range(count):
        print(count)
        shutil.copyfile(infolder+'/render'+str(i)+'/pointcl-nndepth.ply', infolder +'files/nnplyfolder/points'+str(i)+'.ply')
        # shutil.copyfile(infolder+'/render'+str(i)+'/depth.png', infolder +'files/depthfolder/image'+str(i)+'.png')  

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
    model = tensorflow.keras.models.load_model('/home/samir/dbI/models/UN15models/nn1modelold.h5')
    return(model)
# /home/samir/dblive/cnnpredict/models/cnnres01-220-modelwrap1'+'-200-adam-noBN.h5

def load_L_model():
    model = tensorflow.keras.models.load_model('/home/samir/dbI/models/UN15models/nn2salmodel3.h5')
    return(model)

def makemonohigh(folder):
    high = folder + 'high.png'
    colorhigh = cv2.imread(high, 1)
    monohigh = make_grayscale(colorhigh)
    cv2.imwrite(folder+'monohigh.png', monohigh)
    return


def mask(folder):
    color = folder + 'image8.png'
    print('color:', color)
    img1 = np.zeros((H, W), dtype=np.float)
    img1 = cv2.imread(color, 1).astype(np.float32)
    gray = make_grayscale(img1)


    black = folder + 'image9.png'
    img2 = np.zeros((H, W), dtype=np.float)
    img2 = cv2.imread(black, 0).astype(np.float32)
    diff1 = np.subtract(gray, .5*img2)
    mask =  np.zeros((H, W), dtype=np.float)
    for i in range(H):
        for j in range(W):
            if (diff1[i,j]<50):
                mask[i,j]= True
    np.save( folder+ 'mask.npy', mask, allow_pickle=False)
    cv2.imwrite( folder+ 'mask.png', 128*mask)
    return(mask)

def maski(folder,a):
    color = folder + 'image8.png'
    print('color:', color)
    img1 = np.zeros((H, W), dtype=np.float)
    img1 = cv2.imread(color, 1).astype(np.float32)
    gray = make_grayscale(img1)


    black = folder + 'image9.png'
    img2 = np.zeros((H, W), dtype=np.float)
    img2 = cv2.imread(black, 0).astype(np.float32)
    diff1 = np.subtract(gray, .5*img2)
    mask =  np.zeros((H, W), dtype=np.float)
    for i in range(H):
        for j in range(W):
            if (diff1[i,j]<a*10):
                mask[i,j]= True
    np.save( folder+ 'mask.npy', mask, allow_pickle=False)
    cv2.imwrite( folder+ 'mask'+str(a)+'.png', 128*mask)
    print(folder+ 'mask'+str(a)+'.png', str(i))
    return(mask)



def DB_predict( model, x):
    predicted_img = model.predict(np.array([np.expand_dims(x, -1)]))
    predicted_img = predicted_img.squeeze()
    # tensorflow.keras.backend.clear_session()
    return(predicted_img)





def nnHprocess(folder):
    high = folder + 'image0.png' #'blenderimage0.png'
    image1 = cv2.imread(high, 1).astype(np.float32)
    black = folder + 'image9.png' #'' blenderblack.png
    image2 = cv2.imread(black,1).astype(np.float32)
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
    np.save(folder + 'nnwrap1.npy', 2*PI*predicted_img, allow_pickle=False)
    cv2.imwrite( folder + 'nnwrap1.png',255*predicted_img)
    return  #(predicted_img[0], predicted_img[1])


def nnLprocess(folder):
    high = folder + 'nnwrap1.png'
    image = cv2.imread(high, 1).astype(np.float32)
    inp_1 = normalize_image255(image)
    inp_1 = make_grayscale(inp_1)
    mask = np.load(folder+'mask.npy')
    inp_1 = np.multiply(np.logical_not(mask), inp_1)
    mask = np.load(folder+'mask.npy')
    inp_1 = np.multiply(np.logical_not(mask), inp_1)
    # Hmodel = load_H_model()

    start = time.time()
    predicted_img = DB_predict(Lmodel, inp_1)
    end = time.time()
    print('elapsed low:', end-start)
    # mask = np.load(folder+'mask.npy')
    # predicted_img = np.multiply(np.logical_not(mask), predicted_img)


    nnunwrap= (1*predicted_img)
    # nnunwrap= 2*PI*predicted_img
    np.save(folder + 'nnunwrap.npy', nnunwrap, allow_pickle=False)
    # prdicted_img = np.round(predicted_img*17/(np.max(predicted_img)))
    cv2.imwrite( folder + 'nnunwrap.png',nnunwrap)
    # print('255*kdata:', 255*kdata[::40, ::40])


    return  #(predicted_img[0], predicted_img[1])


def unwrap_r(low_f_file, high_f_file, folder):
    filelow = folder + low_f_file
    filehigh = folder +  high_f_file
    wraplow = np.zeros((rheight, rwidth), dtype=np.float64)
    wraphigh = np.zeros((rheight, rwidth), dtype=np.float64)
    unwrapdata = np.zeros((rheight, rwidth), dtype=np.float64)
    im_unwrap = np.zeros((rheight, rwidth), dtype=np.float64)
    wraplow = np.load(filelow)  # To be continued
    wraphigh = np.load(filehigh)
    print('highrange=', np.ptp(wraphigh), np.max(wraphigh), np.min(wraphigh) )
    print('lowrange=', np.ptp(wraplow), np.max(wraplow), np.min(wraplow) )
    # print('high:', wraphigh)
    # print('low:', wraplow)
    
    unwrapdata = np.zeros((rheight, rwidth), dtype=np.float64)
    kdata = np.zeros((rheight, rwidth), dtype=np.int64)
    # wraphigh = cv2.GaussianBlur(wraphigh, (0, 0), 3, 3)
    # wraplow = cv2.GaussianBlur(wraplow, (0, 0), 4, 4)
    for i in range(rheight):
        for j in range(rwidth):
            kdata[i, j] = round((high_freq/low_freq * (wraplow[i, j])- wraphigh[i, j])/(2*PI))
            # unwrapdata[i,j] = .1*(1.1*wraphigh[i, j]/np.max(wraphigh) +2*PI* kdata[i, j]/np.max(wraphigh))
            # unwrapdata[i,j] = 1*(1*wraphigh[i, j] +2*PI* kdata[i, j])
        # if i>140:
        #     for j  in range(160,5):
        #         print('i =', i,
        #         'low:',(wraplow[i, j]),
        #         'high:',wraphigh[i, j],
        #         'round:',round((high_freq/low_freq * (wraplow[i, j])- wraphigh[i, j])/(2*PI))
        #         )
    unwrapdata = np.add(wraphigh, np.multiply(2*PI,kdata) )
    print('kdata:', np.ptp(np.multiply(1,kdata)))
    print('unwrap:', np.ptp(unwrapdata))
    # print("I'm in unwrap_r")
    print('kdata:', kdata[::40, ::40])
    wr_save = folder + 'nnunwrap.npy'
    print(wr_save)
    np.save(wr_save, unwrapdata, allow_pickle=False)
    print('unwrange=', np.ptp(unwrapdata), np.max(unwrapdata), np.min(unwrapdata) )
    k_save = folder + 'nnkdata.npy'
    print(k_save)
    np.save(k_save, kdata, allow_pickle=False)
    # print(wr_save)
    # np.save('wrap24.pickle', wrap24data, allow_pickle=True)
    # unwrapdata = np.multiply(unwrapdata, 1.0)
    # unwrapdata = np.unwrap(np.transpose(unwrapdata))
    # unwrapdata = cv2.GaussianBlur(unwrapdata,(0,0),3,3)
    # unwrapdata = np.multiply(unwrapdata, 1.0)
    maxval = np.amax(unwrapdata)
    print('maxval:', maxval)
    # im_unwrap = 255*unwrapdata/ maxval# np.max(unwrapdata)*255)
    im_unwrap = 3.0*unwrapdata# np.max(unwrapdata)*255)
    # unwrapdata/np.max(unwrapdata)*255
    cv2.imwrite(folder + 'nnunwrap.png', im_unwrap)
    cv2.imwrite(folder + 'nnkdata.png', np.multiply(2*PI,kdata))



def unwrap_k(folder):
    nnkdata = np.zeros((H, W), dtype=np.float64)
    wraphigh = np.zeros((H, W), dtype=np.float64)
    unwrapdata = np.zeros((H, W), dtype=np.float64)
    nnkdata = np.load(folder + '/nnkdata.npy')  # Use a factor of 37.5 when using nnkdata!
    print('nnkdata range = ', np.ptp(nnkdata))

    nnkdata = np.round(40.3*nnkdata)  # Use a factor of 37.5 when using nnkdata!
    # kdata = np.round(kdata/4)
    # kdata = kdata*4
    # kdata = np.matrix.round(45*kdata)

    # wraplow = resize(wraplow, W, H)  # To be continued
    wraphigh = (np.load(folder + '/unwrap1.npy'))
    # wraphigh = wraphigh - np.min(wraphigh)
    # wraphigh = wraphigh/ np.max(wraphigh)
    wraphigh = wraphigh*2*PI
    # print('highrange=', np.ptp(wraphigh), np.max(wraphigh), np.min(wraphigh) )
    # print('nnkdatarange=', np.ptp(nnkdata), np.max(nnkdata), np.min(nnkdata) )
    # wraphigh = normalize_image(wraphigh)
    # wraphigh = 2*PI*wraphigh
    # print('highrange=', np.ptp(wraphigh), np.max(wraphigh), np.min(wraphigh) )
    unwrapdata = np.add(wraphigh, np.multiply(2*PI,nnkdata) )
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
    unwrap = np.load(folder+'/nnunwrap.npy' )
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
    basefile = '/home/samir/Desktop/blender/pycode/bldev2/calplanesL/DDbase.npy'
    DBase = np.load(basefile)
    unwrap = np.load(folder+'nnunwrap.npy' )/2.5
    mask = np.load(folder+'mask.npy' )
    # print('DBase:', np.amax(DBase), np.amin(DBase))
    # print('unwrap:', np.amax(unwrap), np.amin(unwrap))
    depth = np.zeros((rheight, rwidth), dtype=np.float64)
    zee=0
    for i in range(rwidth): #adressing edge noise, can not be explained yet!!!!
        # print('i:', i)
        for j in range(rheight):
            if not(mask[i,j]):

                s=0
                for s in range(0, basecount-1,1):
                    if (unwrap[i,j]< DBase[i,j,s]):
                        ds = (unwrap[i,j] - DBase[i,j,s])/( DBase[i,j,s]- DBase[i,j,s-1])
                        zee = s+ds*1
                        break
                    else:
                        s+=1
                        if s==basecount:
                            print('not found!')

                # print(i,j,unwrap[i,j],DBase[i,j,s])
                if zee == 0:
                    print('not found')
                depth[i,j]= (zee/basecount*-30 + 40)*1

    # print('depth:', np.amax(depth), np.amin(depth))
    print('nndepthrange=', np.ptp(depth), np.max(depth), np.min(depth) )

    im_depth = depth# np.max(unwrapdata)*255)
    cv2.imwrite(folder + 'nndepth.png', im_depth)
    np.save(folder+'nndepth.npy' ,im_depth , allow_pickle=False)


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
                Y = .306 * (v-80) *  Z/80 #.306 = tan(FOV/2) = tan(34/2)
                X = .306 * (u-80) *  Z/80
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


def unw(myfolder):
    unwrap_r('nnwrap2.npy', 'nnwrap1.npy', myfolder )


def makeclouds(scanfolder, count):
     for i in range(count):
        print('start')
        folder = '/home/samir/Desktop/blender/pycode/'+scanfolder+'/render'+ str(i)+'/'
        print(folder)
        if path.exists(folder):
            # generate_pointcloud(folder + 'blendertexture.png', folder + '5mask.png' , folder + 'im_wrap1.png', folder +'pointcl-high.ply')
            # generate_pointcloud(folder + 'blendertexture.png', folder + '-1mask.png' , folder + 'im_wrap2.png', folder +'pointcl-low.ply')
            # generate_pointcloud(folder + 'blendertexture.png', folder + '-1mask.png', folder + 'nnkunwrap.png', folder +'pointcl-unw.ply')
            generate_pointcloud(folder + 'image8.png', folder + 'mask.png', folder + 'nndepth.png', folder +'pointcl-nndepth.ply')



####################################################################################################################

# folder = '/home/samir/serverless/new1-469/1/fringeA/' + str(i)+'.png'
# folder = '/home/samir/Desktop/blender/pycode/bldev2/scans/batchtrain/render'
# bfolder = '/home/samir/Desktop/blender/pycode/bldev2/scans/batchtrain/'
folder ='/home/samir/Desktop/render'
bfolder = '/home/samir/Desktop'
Hmodel = load_H_model()
Lmodel = load_L_model()
offset= 1

for i in range(1):   #(len(os.listdir(bfolder))):
    i = i+offset

    print('i:', i)
    mask(folder+str(i)+'/')
    # unwrap_k(folder + str(i)+'/')
    # makemonohigh(folder+'i')

    nnHprocess(folder + str(i)+'/')
    nnLprocess(folder + str(i)+'/')
    # unw(folder + str(i)+'/')
    start=time.time()
    newDepth(folder+ str(i)+'/' , 30)
    end= time.time()
    print('depth calc time =', end-start)
    nngenerate_pointcloud(folder+str(i) +'/'+ 'image8.png', folder+str(i) +'/'+ 'mask.png', folder+str(i)+'/' + 'nndepth.npy', folder+str(i)+'/' +'pointcl-nndepth.ply')

# getnnplys(bfolder)
# for j in range(10):
#     maski(folder,j)




#========================================================= Parking Lot============================================================



# def repairK(wrapfile, kfile, krepfile):
#     high = wrapfile
#     wdata = cv2.imread(high, 1)
#     krepdata = np.zeros((H, W), dtype=np.float)
#     k = kfile
#     kdata = cv2.imread(k, 1)

#     for j in range(1,160):
#         for i in range(1,160):
#             if ((wdata[i,j][0] - wdata[i-1,j][0])<0):
#                 print('minus')

#                 if ((wdata[i+1,j][0] - wdata[i,j][0])>0):  #bottom spike
#                     krepdata[i,j] = krepdata[i-1,j]+ 7
#                     print('krepdata:', krepdata)
#     cv2.imwrite(krepfile, 3.0*krepdata)



# def unwrap_r(low_f_file, high_f_file, folder):
#     filelow = folder + low_f_file
#     filehigh = folder +  high_f_file
#     wraplow = np.zeros((rheight, rwidth), dtype=np.float64)
#     wraphigh = np.zeros((rheight, rwidth), dtype=np.float64)
#     unwrapdata = np.zeros((rheight, rwidth), dtype=np.float64)
#     im_unwrap = np.zeros((rheight, rwidth), dtype=np.float64)
#     wraplow = np.load(filelow)  # To be continued
#     wraphigh = np.load(filehigh)
#     print('highrange=', np.ptp(wraphigh), np.max(wraphigh), np.min(wraphigh) )
#     print('lowrange=', np.ptp(wraplow), np.max(wraplow), np.min(wraplow) )
#     # print('high:', wraphigh)
#     # print('low:', wraplow)
    
#     unwrapdata = np.zeros((rheight, rwidth), dtype=np.float64)
#     kdata = np.zeros((rheight, rwidth), dtype=np.int64)
#     # wrap1data = cv2.GaussianBlur(wrap1data, (0, 0), 3, 3)
#     # wrap2data = cv2.GaussianBlur(wrap2data, (0, 0), 4, 4)
#     for i in range(rheight):
#         for j in range(rwidth):
#             kdata[i, j] = round((high_freq/low_freq * (wraplow[i, j])- wraphigh[i, j])/(2*PI))
#             # unwrapdata[i,j] = .1*(1.1*wraphigh[i, j]/np.max(wraphigh) +2*PI* kdata[i, j]/np.max(wraphigh))
#             # unwrapdata[i,j] = 1*(1*wraphigh[i, j] +2*PI* kdata[i, j])
#     unwrapdata = np.add(wraphigh, np.multiply(2*PI,kdata) )
#     print('kdata:', np.ptp(np.multiply(1,kdata)))
#     print('unwrap:', np.ptp(unwrapdata))
#     # print("I'm in unwrap_r")
#     print('kdata:', kdata[::40, ::40])
#     wr_save = folder + 'unwrap.npy'
#     np.save(wr_save, unwrapdata, allow_pickle=False)
#     maxval = np.amax(unwrapdata)
#     print('maxval:', maxval)
#     # im_unwrap = 255*unwrapdata/ maxval# np.max(unwrapdata)*255)
#     im_unwrap = 3*unwrapdata# np.max(unwrapdata)*255)
#     # unwrapdata/np.max(unwrapdata)*255
#     cv2.imwrite(folder + 'unwrap.png', im_unwrap)
    # cv2.imwrite(folder + 'kdata.png', np.multiply(2*PI,kdata))


# def unwrap(request):
#     # folder = ScanFolder.objects.last().folderName
#     folder = '/home/samir/db2/scan/static/scan_folder/scan_im_folder/'
#     ref_folder = '/home/samir/db2/scan/static/scan_folder/scan_ref_folder'
#     three_folder = '/home/samir/db2/3D/static/3scan_folder'
#     unwrap_r('scan_wrap2.npy', 'scan_wrap1.npy', folder )
#     deduct_ref('unwrap.npy', 'unwrap.npy', folder, ref_folder)
#     # generate_color_pointcloud(folder + 'image1.png', folder + '/abs_unwrap.png', folder + '/pointcl.ply')
#     generate_json_pointcloud(folder + 'image1.png', folder +
#                              '/abs_unwrap.png', three_folder + '/pointcl.json')
#     return render(request, 'scantemplate.html')



# def unwrap_r(folder):
#     filelow = folder + '/scan_wrap2.npy'
#     filehigh = folder +  '/scan_wrap1.npy'
#     wraplow = np.zeros((H, W), dtype=np.float64)
#     wraphigh = np.zeros((H, W), dtype=np.float64)
#     unwrapdata = np.zeros((H, W), dtype=np.float64)
#     im_unwrap = np.zeros((H, W), dtype=np.float64)
#     wraplow = np.load(filelow)
#     wraplow = resize(wraplow, W, H)  # To be continued
#     wraphigh = np.load(filehigh)
#     wraphigh = resize(wraphigh, W, H)
#     print('highrange=', np.ptp(wraphigh), np.max(wraphigh), np.min(wraphigh) )
#     print('lowrange=', np.ptp(wraplow), np.max(wraplow), np.min(wraplow) )
#     # print('high:', wraphigh)
#     # print('low:', wraplow)
    
#     unwrapdata = np.zeros((H, W), dtype=np.float64)
#     kdata = np.zeros((H, W), dtype=np.int64)
#     # wrap1data = cv2.GaussianBlur(wrap1data, (0, 0), 3, 3)
#     # wrap2data = cv2.GaussianBlur(wrap2data, (0, 0), 4, 4)
#     for i in range(H):
#         for j in range(W):
#             kdata[i, j] = round((high_freq/low_freq * (wraplow[i, j])- wraphigh[i, j])/(2*PI))
#             # unwrapdata[i,j] = .1*(1.1*wraphigh[i, j]/np.max(wraphigh) +2*PI* kdata[i, j]/np.max(wraphigh))
#             # unwrapdata[i,j] = 1*(1*wraphigh[i, j] +2*PI* kdata[i, j])
#     unwrapdata = np.add(wraphigh, np.multiply(2*PI,kdata) )
#     print('kdata:', np.ptp(np.multiply(1,kdata)))
#     print('unwrap:', np.ptp(unwrapdata))
#     # print("I'm in unwrap_r")
#     print('kdata:', kdata[::40, ::40])
#     wr_save = folder + '/unwrap.npy'
#     np.save(wr_save, unwrapdata, allow_pickle=False)
#     maxval = np.amax(unwrapdata)
#     print('maxval:', maxval)
#     # im_unwrap = 255*unwrapdata/ maxval# np.max(unwrapdata)*255)
#     im_unwrap = 3*unwrapdata# np.max(unwrapdata)*255)
#     # unwrapdata/np.max(unwrapdata)*255
#     cv2.imwrite(folder + '/unwrap.png', im_unwrap)
#     cv2.imwrite(folder + '/kdata.png', np.multiply(2*PI,kdata))
#     np.save(folder+'/kdata.npy', kdata, allow_pickle=False )




# def makeDepth(folder, basecount):
#     basefile = '/home/samir/Desktop/blender/pycode/scanplanes/DDbase.npy'
#     DBase = np.load(basefile)
#     # unwrap = np.load(folder+'unwrap.npy' )
#     # print(unwrap.shape)
#     unwrap = cv2.imread(folder + 'nnkunwrap.png', 1).astype(np.float32)
#     unwrap = cv2.cvtColor(unwrap, cv2.COLOR_BGR2GRAY)
#     print(unwrap.shape)
#     # print('DBase:', np.amax(DBase), np.amin(DBase))
#     # print('unwrap:', np.amax(unwrap), np.amin(unwrap))
#     depth = np.zeros((H, W), dtype=np.float64)
#     for i in range(W):
#         # print('i:', i)
#         for j in range(H):
#             s=0
#             for s in range(basecount-1):
#                 if (abs(unwrap[i,j]-DBase[i,j,s])<.15): #used -10 to offset scans449 to avoiod saturation
#                     break
#                 else:
#                     s+=1

#             # print(i,j,unwrap[i,j],DBase[i,j,s])
#             depth[i,j]=s
#             # print('found:',i,j, unwrap[i,j], DBase[i,j,s],s)
    
#     # print('depth:', np.amax(depth), np.amin(depth))
#     im_depth = depth# np.max(unwrapdata)*255)
#     cv2.imwrite(folder + 'nndepth.png', im_depth)
    

# def unw(scanfolder, count):
#     for i in range(count):
#         print('start')

#         folder = '/home/samir/Desktop/blender/pycode/'+scanfolder+'/render'+ str(i)+'/'
#         print(folder)
#         if path.exists(folder):
#             unwrap_r('scan_wrap2.npy', 'scan_wrap1.npy', folder )