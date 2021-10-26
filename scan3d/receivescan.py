"receive"
from pathlib import Path
from shutil import copy2
from compute.settings import DEVICE_PATH, NN_ENABLE
from device.proc import proc_device_data
from utils.img2img import img2img
#from .nn_template.process import process_picture_set
#from .nn.inference.process import proc
from .nn.inference.config import COLOR_FILENAME, FRINGE_FILENAME, NOLIGHT_FILENAME #, POINTCLOUD_JPG_FILENAME
from .preprocessing import preprocessing

if NN_ENABLE:
    from .nn.inference.process_input import process_input_folder

_DEBUG = True
DEVICE_PROCESSING = False

def copy2nn(folder):
    img2img(folder / 'color.jpg', folder / COLOR_FILENAME)
    #img2img(folder / 'dias.jpg', folder / FRINGE_FILENAME)
    img2img(folder / 'nolight.jpg', folder / NOLIGHT_FILENAME)

def receive_scan(deviceid, folder):
    "Receive scan from device"
    if _DEBUG:
        print(f"Receiveing scan from {deviceid} in {folder}")
    # copy file
    #copy2(folder / 'dias.jpg', DEVICE_PATH / deviceid / 'input' / 'last_dias.jpg' )
    copy2nn(folder)
    if DEVICE_PROCESSING:
        proc_device_data(deviceid, folder)
    img2img(folder / 'dias.jpg', folder / FRINGE_FILENAME)
    preprocessing(folder)
    if NN_ENABLE:
        process_input_folder(folder)
    if Path.exists(folder / 'pointcloud.jpg'):
        copy2(folder / 'pointcloud.jpg', DEVICE_PATH / deviceid / 'input' / 'last_dias.jpg' )
