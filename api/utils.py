"""
utils for used in the api view
"""

import os
from pathlib import Path
from shutil import copytree, rmtree #, move
from datetime import datetime
#from compute.settings import  DATA_PATH #BASE_DIR,
#import configparser
#from api.device_config import read_config

INPUT_FOLDER = 'input'
ARCHIVE_FOLDER = 'archive'
ARCHIVE_DATA = False

_DEBUG = False

# def save_uploaded_file(handle, filepath):
#     "save file"
#     with open(filepath, 'wb+') as destination:
#         for chunk in handle.chunks():
#             destination.write(chunk)

def filename_number(filename, number):
    "return new filename whith _number appended to name and same extension"
    name = Path(filename)
    ext = name.suffix
    newname = f'{name.stem}_{number:0=03}{ext}'
    return newname

# def receive_pictures(device, set_number, color_picture, dias_picture, noligt_picture):
#     # receive jpg pictures and save in input folder with set_number
#     folder = DATA_PATH / device / 'input'
#     os.makedirs(folder, exist_ok=True)
#     number = f"_{int(set_number):03d}"
#     color_pic = "color" + number + ".jpg"
#     dias_pic = "dias" + number + ".jpg"
#     nolight_pic = "nolight" + number + ".jpg"
#     save_uploaded_file(color_picture, folder / color_pic )
#     save_uploaded_file(dias_picture, folder / dias_pic )
#     save_uploaded_file(noligt_picture, folder / nolight_pic )
#     return True

def start_scan(device, device_path):
    "common start scan operations"
    if _DEBUG:
        print("Start scan:", device, device_path)
    infolder = Path(device_path) / INPUT_FOLDER
    if ARCHIVE_DATA:
    # archive last input folder
        if os.path.exists(infolder):
            datestr = datetime.now().strftime('%y%m%d-%H%M%S')
            outfolder = device_path / ARCHIVE_FOLDER / datestr
            # infolder  = device_path /'dummy'
            # move(infolder,outfolder)
            #os.rename(str(infolder),str(outfolder))
            #Path(infolder).rename(outfolder)
            copytree(infolder, outfolder, dirs_exist_ok=True)
    # clean folder
    rmtree(infolder, ignore_errors=True)
    os.makedirs(infolder, exist_ok=True)

def stop_scan(device, device_path):
    "common stop_scan operations"
    if _DEBUG:
        print("Stop scan:", device, device_path)
