import numpy as np
import cv2
from compute.settings import DATA_PATH

MODEL_PATH = DATA_PATH / 'nnmodels/'
DDBASE="DDbase.npy"
DEPTH_DB = MODEL_PATH / DDBASE

rwidth = 160
rheight = 160

_DEBUG = False

def newDepth(folder, basecount):
    #basefile = '/home/samir/Desktop/blender/pycode/bldev2/calplanes/DDbase.npy'
    DBase = np.load(str(DEPTH_DB))
    unwrap = np.load(str(folder / 'nnunwrap.npy'))/3
    mask = np.load(str(folder / 'mask.npy') )
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
                            print('s==bascount not found!')

                # print(i,j,unwrap[i,j],DBase[i,j,s])
                if zee == 0:
                    print('zee=0 not found')
                depth[i,j]= (zee/basecount*-30 + 40)*1

    # print('depth:', np.amax(depth), np.amin(depth))
    if _DEBUG:
        print('nndepthrange=', np.ptp(depth), np.max(depth), np.min(depth) )

    im_depth = depth# np.max(unwrapdata)*255)
    cv2.imwrite(str (folder / 'nndepth.png'), im_depth)
    np.save(str(folder/'nndepth.npy') ,im_depth , allow_pickle=False)

    # call addWeighted function. use beta = 0 to effectively only operate one one image
    brightness = 1
    contrast = 5
    out = cv2.addWeighted( im_depth, contrast, im_depth, 0, brightness)
    cv2.imwrite(str (folder / 'nndepth2.png'), out)
    