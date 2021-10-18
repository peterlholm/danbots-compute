"""
utils for used in the api view
"""

import os
from shutil import copytree, rmtree
from datetime import datetime
from compute.settings import DATA_PATH
#import configparser
#from api.device_config import read_config

INPUT_FOLDER = 'input'
ARCHIVE_FOLDER = 'archive'
ARCHIVE_DATA = True

_DEBUG = False

def save_uploaded_file(handle, filepath):
    with open(filepath, 'wb+') as destination:
        for chunk in handle.chunks():
            destination.write(chunk)

def receive_pictures(device, set_number, color_picture, dias_picture, noligt_picture):
    # receive jpg pictures and save in input folder with set_number
    folder = DATA_PATH / device / 'input'
    os.makedirs(folder, exist_ok=True)
    number = f"_{int(set_number):03d}"
    color_pic = "color" + number + ".jpg"
    dias_pic = "dias" + number + ".jpg"
    nolight_pic = "nolight" + number + ".jpg"
    save_uploaded_file(color_picture, folder / color_pic )
    save_uploaded_file(dias_picture, folder / dias_pic )
    save_uploaded_file(noligt_picture, folder / nolight_pic )
    return True

def start_scan(device, device_path):
    # archive last input folder
    if _DEBUG:
        print("Start scan:", device, device_path)
    infolder = device_path / INPUT_FOLDER
    os.makedirs(infolder, exist_ok=True)
    if ARCHIVE_DATA:
        if os.path.exists(infolder):
            datestr = datetime.now().strftime('%y%m%d-%H%M%S')
            outfolder = device_path / ARCHIVE_FOLDER / datestr
            copytree(infolder, outfolder, dirs_exist_ok=True)
    # clean folder
    rmtree(infolder)
    os.makedirs(infolder, exist_ok=True)

def stop_scan(device, device_path):
    if _DEBUG:
        print("Stop scan:", device, device_path)
