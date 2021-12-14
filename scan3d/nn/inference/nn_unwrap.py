"nn unwrapping"
import numpy as np
import cv2

H = 160
W = 160
PI = np.pi

def unwrap_k(folder):
    nnkdata = np.zeros((H, W), dtype=np.float64)
    wraphigh = np.zeros((H, W), dtype=np.float64)
    unwrapdata = np.zeros((H, W), dtype=np.float64)
    nnkdata = np.load(folder / 'nnkdata.npy')  # Use a factor of 37.5 when using nnkdata!
    #print('nnkdata range = ', np.ptp(nnkdata))

    # nnkdata = np.round(40.3*nnkdata)  # Use a factor of 37.5 when using nnkdata!
    # kdata = np.round(kdata/4)
    # kdata = kdata*4
    # kdata = np.matrix.round(45*kdata)

    # wraplow = resize(wraplow, W, H)  # To be continued
    wraphigh = (np.load(folder / 'nnwrap1.npy'))
    # wraphigh = wraphigh - np.min(wraphigh)
    # wraphigh = wraphigh/ np.max(wraphigh)
    # wraphigh = wraphigh*2*PI
    # print('highrange=', np.ptp(wraphigh), np.max(wraphigh), np.min(wraphigh) )
    # print('nnkdatarange=', np.ptp(nnkdata), np.max(nnkdata), np.min(nnkdata) )
    # wraphigh = normalize_image(wraphigh)
    # wraphigh = 2*PI*wraphigh
    # print('highrange=', np.ptp(wraphigh), np.max(wraphigh), np.min(wraphigh) )
    unwrapdata = np.add(wraphigh, np.multiply(2*PI,nnkdata) )
    #print('nnunwrange=', np.ptp(unwrapdata), np.max(unwrapdata), np.min(unwrapdata) )
    wr_save = folder / 'nnkunwrap.npy'
    np.save(str(wr_save), unwrapdata, allow_pickle=False)
    cv2.imwrite(str(folder / 'nnkunwrap.png'), 3.0*unwrapdata)
