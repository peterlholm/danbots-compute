import os
from compute.settings import DATA_PATH
import configparser
from api.device_config import read_config

def save_uploaded_file(handle, filepath):
    with open(filepath, 'wb+') as destination:
        for chunk in handle.chunks():
            destination.write(chunk)

def receive_pictures(device, set_number, color_picture, dias_picture, noligt_picture):
    # receive jpg pictures and save in input folder with set_number
    folder = DATA_PATH / device / 'input'
    os.makedirs(folder, exist_ok=True)
    number = "_{0:03d}".format(int(set_number))
    color_pic = "color" + number + ".jpg"
    dias_pic = "dias" + number + ".jpg"
    nolight_pic = "nolight" + number + ".jpg"
    save_uploaded_file(color_picture, folder / color_pic )
    save_uploaded_file(dias_picture, folder / dias_pic )
    save_uploaded_file(noligt_picture, folder / nolight_pic )
    return True
