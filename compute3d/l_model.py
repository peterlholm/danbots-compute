import time
import numpy as np
import cv2
import tensorflow.keras
from PIL import Image
from compute.settings import DATA_PATH
from compute3d.nn_util import make_grayscale, db_predict

MODEL_PATH = DATA_PATH / 'nnmodels/'
L_MODELFILE = 'UN15-680-mat-b8-Wrap-100-V2.h5'

RWIDTH = 160
RHEIGHT = 160

def load_l_model():
    model = tensorflow.keras.models.load_model(MODEL_PATH / L_MODELFILE)
    return model

def normalize_image(img):
    # Normalizes the input image to range (0, 1) for visualization
    img = img - np.min(img)
    img = img/np.max(img)
    return img

def normalize_image255(img):
    # Changes the input image range from (0, 255) to (0, 1)number_of_epochs = 5
    img = img/255.0
    return img

def nn_llprocess(folder):
    high = folder / 'unwrap1.png'
    image = cv2.imread(str(high), 1).astype(np.float32)
    inp_1 = normalize_image255(image)
    inp_1 = make_grayscale(inp_1)
    # mask = np.load(folder+'mask.npy')
    # inp_1 = np.multiply(np.logical_not(mask), inp_1)
    # Hmodel = load_H_model()

    start = time.time()
    predicted_img = db_predict(Lmodel, inp_1)
    end = time.time()
    print('elapsed low:', end-start)

    # mask = np.load(str(folder / 'mask.npy'))    commentet - not used

    unwdata = predicted_img # mask is not calculated properly
    # unwdata = np.multiply(np.logical_not(mask), predicted_img)
    # kdatay = 255/6*predicted_img
    # kdatay = np.round(kdatay)
    # print('kdatay:', kdatay[::40, ::40])
    np.save(str(folder / 'nnunwrap.npy'), 80*unwdata, allow_pickle=False)
    # prdicted_img = np.round(predicted_img*17/(np.max(predicted_img)))
    cv2.imwrite( str(folder / 'nnunwrap.png'),255*unwdata)
    # print('255*kdata:', 255*kdata[::40, ::40])


    return  #(predicted_img[0], predicted_img[1])

def new_ddddepth(folder, basecount):
    basefile = MODEL_PATH / 'DDbase.npy'
    d_base = np.load(basefile)
    unwrap = np.load(str(folder / 'nnunwrap.npy') )
    mask = np.load(str(folder / 'mask.npy') )
    # print('DBase:', np.amax(DBase), np.amin(DBase))
    # print('unwrap:', np.amax(unwrap), np.amin(unwrap))
    depth = np.zeros((RHEIGHT, RWIDTH), dtype=np.float64)
    zee=0
    for i in range(RWIDTH):
        # print('i:', i)
        for j in range(RHEIGHT):
            if not(mask[i,j]):

                s=0
                for s in range(0, basecount-1,10):
                    if (unwrap[i,j]< d_base[i,j,s]):
                        ds = (unwrap[i,j] - d_base[i,j,s])/( d_base[i,j,s]- d_base[i,j,s-10])
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
            if mask.getpixel((v,u))<55:
                # Z = depth.getpixel((u, v))
                Z = depth[u,v]
                if Z < 0:
                    Z = 0
                else:
                    if Z> 80:
                        Z = 80
                if Z == 0:
                    continue
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



Lmodel = load_l_model()

def l_process_input(folder):
    nn_llprocess(folder)
    new_ddddepth(folder, 200)
    nngenerate_pointcloud(folder+'/'+ 'image8.png', folder+'/'+ 'mask.png', folder+'/' + 'nndepth.npy', folder+'/' +'pointcl-nndepth.ply')
