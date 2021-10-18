from pathlib import Path
import cv2
import numpy as np
import tensorflow.keras

from compute.settings import DATA_PATH
from nn.inference.config import COLOR_FILENAME, NOLIGHT_FILENAME
from nn.inference.create_mask import create_mask
from nn.inference.nn_util import make_grayscale, normalize_image255, db_predict
import time

MODEL_PATH = DATA_PATH / 'nnmodels/'
H_MODELFILE = 'UN15-680-mat-b8-Wrap-100-V2.h5'

COLOR_IMAGE = 'color.png'

def load_h_model():
    model = tensorflow.keras.models.load_model(MODEL_PATH / H_MODELFILE)
    return model

Hmodel = load_h_model()

def nn_h_process(folder):
    high = folder / COLOR_IMAGE
    image1 = cv2.imread(str(high), 1).astype(np.float32)
    image = image1
    inp_1 = normalize_image255(image)
    inp_1 = make_grayscale(inp_1)

    start = time.time()
    predicted_img = db_predict(Hmodel, inp_1)
    end = time.time()
    print('elapsed high:', end-start)

    # mask = np.load(folder+'mask.npy')
    # wrapH = np.multiply(np.logical_not(mask), predicted_img)
    # wrapH = resize(wrapH, W, H)
    np.save(folder / 'unwrap1.npy', predicted_img, allow_pickle=False)
    cv2.imwrite( str(folder / 'unwrap1.png'),255*predicted_img)
    return  #(predicted_img[0], predicted_img[1])



def wrap_net(folder):
    start = time.time()
    infolder = Path(folder)
    create_mask(infolder / COLOR_FILENAME, infolder / NOLIGHT_FILENAME, folder)
    #mask(folder)
    nn_h_process(folder)
    end = time.time()
    print('Wrap_net Processing time  {:.2f} sec'.format(end-start))
    return
