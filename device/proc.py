"""
Process date acoording to device parameters
"""
from os import read
from api.device_config import read_device_config, save_device_config
from scan3d.nn.inference.config import FRINGE_FILENAME
from utils.img_utils import rotate_img
_DEBUG=True

def proc_device_data(device, folder):
    if _DEBUG:
        print(f"Device specifix processing, device: {device} folder: {folder}")

    config = read_device_config(device)
    slope = float(config['calibrate']['slope'])
    print("slope", slope)
    rotate_img(folder / 'dias.jpg', -slope*30.0, folder / 'fringe.png')
    return True

