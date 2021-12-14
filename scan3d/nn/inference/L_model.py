"L_model"
import cv2
import numpy as np
import tensorflow.keras
from compute.settings import  MODEL_PATH #DATA_PATH,
from .nn_util import normalize_image255, make_grayscale, db_predict
from .config import COLOR_FILENAME, NOLIGHT_FILENAME

#MODEL_PATH = DATA_PATH / 'nnmodels/'
#L_MODELFILE = 'wr1uwr.h5'
L_MODELFILE = 'L_model.h5'

COLOR_IMAGE = 'color.png'

_DEBUG = False

def load_L_model():
    model = tensorflow.keras.models.load_model(MODEL_PATH / L_MODELFILE)
    if _DEBUG:
        print("L model Loaded")
    return model

Lmodel = load_L_model()

def nnLprocess(folder):
    high = folder / 'nnwrap1.png'
    image = cv2.imread(str(high), 1).astype(np.float32)
    inp_1 = normalize_image255(image)
    inp_1 = make_grayscale(inp_1)
    # mask = np.load(folder+'mask.npy')
    # inp_1 = np.multiply(np.logical_not(mask), inp_1)
    # Hmodel = load_H_model()

    #start = time.time()
    predicted_img = db_predict(Lmodel, inp_1)
    #end = time.time()
    #print('elapsed low:', end-start)
    #print (predicted_img.shape)
    predicted_img = np.argmax(predicted_img, axis=-1)
    #mask = np.load(folder+'mask.npy')
    nnkdata = predicted_img # mask is not calculated properly
    # unwdata = np.multiply(np.logical_not(mask), predicted_img)
    # kdatay = 255/6*predicted_img
    # kdatay = np.round(kdatay)
    #print('kdata:', nnkdata[::40, ::40])
    np.save(str(folder / 'nnkdata.npy'), 1*nnkdata, allow_pickle=False)
    # prdicted_img = np.round(predicted_img*17/(np.max(predicted_img)))
    cv2.imwrite( str(folder / 'nnkdata.png'),1*nnkdata)
    # print('255*kdata:', 255*kdata[::40, ::40])


    return  #(predicted_img[0], predicted_img[1])


# def nnLprocess(folder):
#     high = folder / 'nnwrap1.png'
#     image = cv2.imread(str(high), 1).astype(np.float32)
#     inp_1 = normalize_image255(image)
#     inp_1 = make_grayscale(inp_1)
#     # mask = np.load(folder+'mask.npy')
#     # inp_1 = np.multiply(np.logical_not(mask), inp_1)
#     # mask = np.load(folder+'mask.npy')
#     # inp_1 = np.multiply(np.logical_not(mask), inp_1)
#     # Hmodel = load_H_model()

#     #start = time.time()
#     predicted_img = db_predict(Lmodel, inp_1)
#     #end = time.time()
#     #print('elapsed low:', end-start)
#     # mask = np.load(folder+'mask.npy')
#     # predicted_img = np.multiply(np.logical_not(mask), predicted_img)

#     PI = np.pi
#     #nnunwrap= (255*predicted_img)
#     nnunwrap= (predicted_img)

#     #nnunwrap= 2*PI*predicted_img

#     np.save(str(folder / 'nnunwrap.npy'), nnunwrap, allow_pickle=False)
#     # prdicted_img = np.round(predicted_img*17/(np.max(predicted_img)))
#     cv2.imwrite( str(folder / 'nnunwrap.png'),nnunwrap)
#     # print('255*kdata:', 255*kdata[::40, ::40])


#     return  #(predicted_img[0], predicted_img[1])


def process_lmodel(folder):
    nnLprocess(folder)
    