"numpu utils"
import numpy as np
import cv2

_DEBUG = False

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

def add_0mask(np_in, mask_in):
    #print(npin.shape)
    #newpic = np.zeros((np_in.shape[0],np_in.shape[1]), dtype=np.float)
    for x in range(0,np_in.shape[0]):
        for y in range(0,np_in.shape[1]):
            #print (x,y,npin[x,y])
            #newmask[x,y] = np_in[x,y]
            if mask_in[x,y] == 0:
                np_in[x,y] = 0
    return np_in

def add_0mask_file(np_filename, maskfilename, outfilename):
    _fil = np.load(np_filename, allow_pickle=True)
    _mask = np.load(maskfilename)
    _newnp = add_0mask(_fil, _mask)
    np.save(outfilename, _newnp, allow_pickle=False)
    if _DEBUG:
        print("max", np.max(_newnp))
        cv2.imwrite( "new0pic.png", _newnp)

def mask_file(np_filename, maskfilename, outfilename):
    _fil = np.load(np_filename)
    _mask = np.load(maskfilename)
    _newnp = add_mask(_fil, _mask)
    np.save(outfilename, _newnp, allow_pickle=False)
    if _DEBUG:
        print("max", np.max(_newnp))
        fac = 255 / np.max(_newnp)
        cv2.imwrite( "newmask.png", fac*_newnp)

def multiply(infile, outfile, tal):
    img = cv2.imread(str(infile), 1).astype(np.float32)
    img = tal * img
    cv2.imwrite( str(outfile), img)

if __name__ == '__main__':
    mymask = "testdata/okt25/render5/mask.npy"
    wrap = "testdata/okt25/render5/nnunwrap.npy"
    mask_file(wrap, mymask, "outmask.npy")
