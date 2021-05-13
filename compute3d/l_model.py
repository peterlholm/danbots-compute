import time
import numpy as np
import cv2
import tensorflow.keras
from PIL import Image
from compute.settings import DATA_PATH
from compute3d.nn_util import make_grayscale, db_predict, normalize_image255

MODEL_PATH = DATA_PATH / 'nnmodels/'
L_MODELFILE = 'UN15may-44x-dentmix-Kunw-b8-200.h5'

rwidth = 160
rheight = 160
H =160
W = 160
PI = np.pi


def load_l_model():
    model = tensorflow.keras.models.load_model(MODEL_PATH / L_MODELFILE)
    return model

def nn_llprocess(folder):
    high = folder / 'unwrap1.png'
    image = cv2.imread(str(high), 1).astype(np.float32)
    inp_1 = normalize_image255(image)
    inp_1 = make_grayscale(inp_1)
    mask = np.load(folder / 'mask.npy')
    inp_1 = np.multiply(np.logical_not(mask), inp_1)
    # mask = np.load(folder+'mask.npy')
    # inp_1 = np.multiply(np.logical_not(mask), inp_1)
    # Hmodel = load_H_model()

    start = time.time()
    predicted_img = db_predict(Lmodel, inp_1)
    end = time.time()
    print('elapsed low:', end-start)
    mask = np.load(folder /'mask.npy')
    predicted_img = np.multiply(np.logical_not(mask), predicted_img)


    nnkdata= 3*(np.round((255*predicted_img)/3))
    np.save(str(folder / 'nnkdata.npy'), nnkdata/255, allow_pickle=False)
    # prdicted_img = np.round(predicted_img*17/(np.max(predicted_img)))
    cv2.imwrite( str(folder / 'nnkdata.png'),nnkdata)
    # print('255*kdata:', 255*kdata[::40, ::40])


    return  #(predicted_img[0], predicted_img[1])

def unwrap_k(folder):
    nnkdata = np.zeros((H, W), dtype=np.float64)
    wraphigh = np.zeros((H, W), dtype=np.float64)
    unwrapdata = np.zeros((H, W), dtype=np.float64)
    nnkdata = np.load(str(folder / 'nnkdata.npy'))  # Use a factor of 37.5 when using nnkdata!

    nnkdata = np.round(40*nnkdata)  # Use a factor of 37.5 when using nnkdata!
    # kdata = np.round(kdata/4)
    # kdata = kdata*4
    # kdata = np.matrix.round(45*kdata)

    # wraplow = resize(wraplow, W, H)  # To be continued
    wraphigh = (np.load(str(folder / 'unwrap1.npy')))
    # wraphigh = wraphigh - np.min(wraphigh)
    # wraphigh = wraphigh/ np.max(wraphigh)
    wraphigh = wraphigh*2*PI
    print('highrange=', np.ptp(wraphigh), np.max(wraphigh), np.min(wraphigh) )
    print('nnkdatarange=', np.ptp(nnkdata), np.max(nnkdata), np.min(nnkdata) )
    # wraphigh = normalize_image(wraphigh)
    # wraphigh = 2*PI*wraphigh
    # print('highrange=', np.ptp(wraphigh), np.max(wraphigh), np.min(wraphigh) )
    unwrapdata = np.add(wraphigh, np.multiply(2*PI,nnkdata) )
    print('nnkdata:', nnkdata[::40, ::40])
    print('nnunwrange=', np.ptp(unwrapdata), np.max(unwrapdata), np.min(unwrapdata) )
    wr_save = folder / 'nnkunwrap.npy'
    np.save(wr_save, unwrapdata, allow_pickle=False)
    cv2.imwrite(str(folder / 'nnkunwrap.png'), 3.0*unwrapdata)

def new_depth(folder, basecount):
    basefile = MODEL_PATH / 'DDbase.npy'
    DBase = np.load(basefile)
    unwrap = np.load(folder / 'nnkunwrap.npy' )
    mask = np.load(folder /'mask.npy' )
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
                        if s==200:
                            print('not found!')

                # print(i,j,unwrap[i,j],DBase[i,j,s])
                if zee == 0:
                    print('not found')
                depth[i,j]= (zee/200*-20 + 40)*1

    # print('depth:', np.amax(depth), np.amin(depth))
    print('nndepthrange=', np.ptp(depth), np.max(depth), np.min(depth) )

    im_depth = depth # np.max(unwrapdata)*255)
    cv2.imwrite(str(folder / 'nndepth.png'), im_depth)
    np.save(folder / 'nndepth.npy' ,im_depth , allow_pickle=False)

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
    start = time.time()
    nn_llprocess(folder)
    unwrap_k(folder)
    new_depth(folder, 200)
    nngenerate_pointcloud(str(folder / 'image8.png'), str(folder / 'mask.png'), str(folder / 'nndepth.npy'), str(folder / 'pointcl-nndepth.ply'))
    end = time.time()
    return {'l_process_time': end-start}


    # nnLprocess(folder + str(i)+'/')
    # unwrap_k(folder + str(i)+'/')
    # newDepth(folder+ str(i)+'/' , 200)
    # nngenerate_pointcloud(folder+str(i) +'/'+ 'image8.png', folder+str(i) +'/'+ 'mask.png', folder+str(i)+'/' + 'nndepth.npy', folder+str(i)+'/' +'pointcl-nndepth.ply')
