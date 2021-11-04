"Receive a scanner data set do device preprocessing and prepare it for NN"
from pathlib import Path
from shutil import copy2
from compute.settings import DEVICE_PATH, NN_ENABLE
from device.device_proc import proc_device_data
from utils.img2img import img2img
from utils.histoimg import histo_img
from .nn.inference.config import COLOR_FILENAME, FRINGE_FILENAME, NOLIGHT_FILENAME #, POINTCLOUD_JPG_FILENAME
from .processing import general_postprocessing, scan_preprocessing

if NN_ENABLE:
    from .nn.inference.process_input import process_input_folder

_DEBUG = True
DEVICE_PROCESSING = True

def copy2nn(folder):
    img2img(folder / 'color.jpg', folder / COLOR_FILENAME)
    img2img(folder / 'dias.jpg', folder / FRINGE_FILENAME)
    img2img(folder / 'nolight.jpg', folder / NOLIGHT_FILENAME)

def receive_scan(deviceid, folder):
    "Receive scan from device: color.jpg, dias.jpg, nolight.jpg"
    if _DEBUG:
        print(f"Receiveing scan from {deviceid} in {folder}")
        histo_img(folder / 'color.jpg', folder / 'color_histo.jpg')
        histo_img(folder / 'dias.jpg', folder / 'dias_histo.jpg')
        histo_img(folder / 'nolight.jpg', folder / 'nolight_histo.jpg')
    copy2(folder / 'dias.jpg', DEVICE_PATH / deviceid / 'input' / 'last_dias.jpg' )
    if DEVICE_PROCESSING:
        proc_device_data(deviceid, folder)
    else:
        copy2nn(folder)
    scan_preprocessing(folder)  # change contrast etc
    general_postprocessing(folder)
    # here the color.png, fringe.png, nolight.png is expected
    if NN_ENABLE:
        process_input_folder(folder)
    if Path.exists(folder / 'pointcloud.jpg'):
        copy2(folder / 'pointcloud.jpg', DEVICE_PATH / deviceid / 'input' / 'last_dias.jpg' )
        copy2(folder / 'pointcloud.jpg', DEVICE_PATH / deviceid / 'input' / 'last_pointcloud.jpg' )
