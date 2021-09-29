import cv2
import numpy as np

def make_grayscale(img):
    # Transform color image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray_img

def normalize_image255(img):
    # Changes the input image range from (0, 255) to (0, 1)number_of_epochs = 5
    img = img/255.0
    return img

def db_predict( model, x):
    predicted_img = model.predict(np.array([np.expand_dims(x, -1)]))
    predicted_img = predicted_img.squeeze()
    # tensorflow.keras.backend.clear_session()
    return predicted_img
