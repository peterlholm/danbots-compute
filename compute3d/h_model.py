import time
import numpy as np
import cv2
import tensorflow.keras
from compute.settings import DATA_PATH

MODEL_PATH = DATA_PATH / 'nnmodels/'
#H_MODELFILE = 'UN30-400-WUN-100-V2.h5'
H_MODELFILE = 'UN15-680-mat-b8-Wrap-100-V2.h5'

H =160
W = 160

#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def load_h_model():
    model = tensorflow.keras.models.load_model(MODEL_PATH / H_MODELFILE)
    return model

Hmodel = load_h_model()

def make_grayscale(img):
    # Transform color image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray_img

def mask(folder):
    color = folder / 'image8.png'
    print('color:', color)
    img1 = np.zeros((H, W), dtype=np.float)
    img1 = cv2.imread(str(color), 1).astype(np.float32)
    gray = make_grayscale(img1)
    black = folder / 'image9.png'
    img2 = np.zeros((H, W), dtype=np.float)
    img2 = cv2.imread(str(black), 0).astype(np.float32)
    diff1 = np.subtract(gray, .5*img2)
    mask =  np.zeros((H, W), dtype=np.float)
    for i in range(H):
        for j in range(W):
            if (diff1[i,j]<50):
                mask[i,j]= True
    np.save( folder / 'mask.npy', mask, allow_pickle=False)
    cv2.imwrite( str(folder / 'mask.png'), 128*mask)
    return mask


def normalize_image255(img):
    # Changes the input image range from (0, 255) to (0, 1)number_of_epochs = 5
    img = img/255.0
    return img


def DB_predict( model, x):
    predicted_img = model.predict(np.array([np.expand_dims(x, -1)]))
    predicted_img = predicted_img.squeeze()
    # tensorflow.keras.backend.clear_session()
    return predicted_img



def nnHprocess(folder):
    high = folder / 'image0.png' #'blenderimage0.png' or 'image0.png'
    image1 = cv2.imread(str(high), 1).astype(np.float32)
    # black = folder + 'image9.png' #'' blenderblack.png or 'image9.png'
    # image2 = cv2.imread(black,1).astype(np.float32)
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
    np.save(folder / 'unwrap1.npy', predicted_img, allow_pickle=False)
    cv2.imwrite( str(folder / 'unwrap1.png'),255*predicted_img)
    return  #(predicted_img[0], predicted_img[1])


def nnprocess_input(folder):
    mask(folder)
    nnHprocess(folder)
    return
