#import os
#from time import sleep
from datetime import datetime
#from pathlib import Path
import threading
from PIL import Image, ImageOps
#from compute3d.UNTruepredictV3 import nnprocess_input
from compute3d.h_model import h_process_input
from compute3d.l_model import l_process_input

COLOR_PICTURE = 'image8.jpg'
DIAS_PICTURE = 'image0.jpg'     # in b/w
NOLIGHT_PICTURE = 'image9.jpg'
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

def background(myfunction):
    '''
    a threading decorator
    use @background above the function you want to run in the background
    '''
    def bg_f(*a, **kw):
        print(myfunction.__name__)
        threading.Thread(target=myfunction, name=myfunction.__name__, args=a, kwargs=kw).start()
    return bg_f

def convert_picture(filepath, outfilepath):
    """ Convert from jpg to png """
    im1 = Image.open(filepath)
    im1.save(outfilepath)

def convert_blackwhite(filepath, outfilepath):
    """ convert from any(jpg,png) to greyscale (jpg,png) """
    im1 = Image.open(filepath)
    grey = ImageOps.grayscale(im1)
    grey.save(outfilepath)

#@background
def process_input(folder):
    """ Process a incoming folder with a pictureset """
    print("Processeing", folder)

    convert_picture(folder / COLOR_PICTURE, folder /'image8.png')
    convert_picture(folder / DIAS_PICTURE, folder /'image0C.png')
    convert_picture(folder / NOLIGHT_PICTURE, folder /'image9.png')
    convert_blackwhite(folder / COLOR_PICTURE, folder / 'image0.png')

    print (datetime.now().isoformat(),"calling nnprocess_input")
    h_process_input(folder)

    print ("processing finish")

def test_process_input(folder):
    """ Process a incoming folder with a pictureset """
    print("Test Processeing", folder)
    print ("calling nnprocess_input")
    h_result = h_process_input(folder)
    print("H_result", h_result)
    l_result = l_process_input(folder)
    print("L_result", h_result)

    print ("processing finish")
    return { **h_result, **l_result }
