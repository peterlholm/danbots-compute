"numpu utils"
import numpy as np
import cv2

_DEBUG = True

def add_mask(np_in, mask_in):
    #print(npin.shape)
    newmask = np.zeros((np_in.shape[0],np_in.shape[1]), dtype=np.float)
    for x in range(0,np_in.shape[0]):
        for y in range(0,np_in.shape[1]):
            #print (x,y,npin[x,y])
            newmask[x,y] = np_in[x,y]
            if mask_in[x,y] == 1:
                newmask[x,y] = 1
    return newmask

def maskedfile(np_filename, maskfilename, outfilename):
    _fil = np.load(np_filename)
    _mask = np.load(maskfilename)
    _newnp = add_mask(_fil, _mask)
    np.save(outfilename, _newnp, allow_pickle=False)
    if _DEBUG:
        print("max", np.max(_newnp))
        fac = 255 / np.max(_newnp)
        cv2.imwrite( "newmask.png", fac*_newnp)

if __name__ == '__main__':
    mymask = "testdata/okt25/render5/mask.npy"
    wrap = "testdata/okt25/render5/nnunwrap.npy"
    fil = np.load(wrap)
    mask = np.load(mymask)
    newmask1 = add_mask(fil, mask)

    np.save( "newmask.npy", newmask1, allow_pickle=False)
    cv2.imwrite( "newmask.png", 128*newmask1)
