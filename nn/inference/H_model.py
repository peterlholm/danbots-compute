#import math
import cv2
import numpy as np
import tensorflow.keras
from compute.settings import DATA_PATH
from nn.inference.nn_util import normalize_image255, make_grayscale, db_predict
from nn.inference.config import COLOR_FILENAME, NOLIGHT_FILENAME

MODEL_PATH = DATA_PATH / 'nnmodels/'
H_MODELFILE = 'im0wr40.h5'

COLOR_IMAGE = 'color.png'
PI = np.pi

def load_h_model():
    model = tensorflow.keras.models.load_model(MODEL_PATH / H_MODELFILE)
    print("H model loaded")
    return model

Hmodel = load_h_model()

def nnHprocess(folder):
    high = folder / COLOR_IMAGE #'blenderimage0.png'
    image1 = cv2.imread(str(high), 1).astype(np.float32)
    #black = folder + 'image9.png' #'' blenderblack.png
    #image2 = cv2.imread(black,1).astype(np.float32)
    image = image1 #- image2
    inp_1 = normalize_image255(image)
    inp_1 = make_grayscale(inp_1)
    # mask = np.load(folder+'mask.npy')
    # inp_1 = np.multiply(np.logical_not(mask), inp_1)
    # Hmodel = load_H_model()

    #start = time.time()
    predicted_img = db_predict(Hmodel, inp_1)
    #end = time.time()
    #print('elapsed high:', end-start)

    # mask = np.load(folder+'mask.npy')
    # wrapH = np.multiply(np.logical_not(mask), predicted_img)
    # wrapH = resize(wrapH, W, H)
    np.save(folder / 'nnwrap1.npy', 2*PI*predicted_img, allow_pickle=False)
    cv2.imwrite( str(folder / 'nnwrap1.png'),255*predicted_img)
    return  #(predicted_img[0], predicted_img[1])



def process_hmodel(folder):
    nnHprocess(folder)