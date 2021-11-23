"Receive a scanner data set do device preprocessing and prepare it for NN"
from pathlib import Path
from shutil import copy2

from matplotlib.pyplot import sca
from compute.settings import DEVICE_PATH, NN_ENABLE
from device.device_proc import proc_device_data
from utils.img2img import img2img
from utils.img_utils import change_contrast_brightness
from utils.pcl_utils import ply2jpg
from utils.histoimg import histo_img
from .nn.inference.config import COLOR_FILENAME, FRINGE_FILENAME, NOLIGHT_FILENAME #, POINTCLOUD_JPG_FILENAME
from .processing import general_postprocessing
from .filtering import radius_outliersremoval, scan_filter

if NN_ENABLE:
    from .nn.inference.process_input import process_input_folder

_DEBUG = True
DEVICE_PROCESSING = False
EXPOSURE_PROCESSING = False
CONTRAST = 1.7
BRIGHTNESS = 0.9

def copy2png(folder):
    img2img(folder / 'color.jpg', folder / COLOR_FILENAME)
    img2img(folder / 'dias.jpg', folder / FRINGE_FILENAME)
    img2img(folder / 'nolight.jpg', folder / NOLIGHT_FILENAME)

def change_exposure(infile, outfile):
    change_contrast_brightness(infile, outfile, contrast=CONTRAST, brightness=BRIGHTNESS)

def process_scan(deviceid, folder):
    "receive png files"
    if _DEBUG:
        print(f"Receiveing scan from {deviceid} in {folder}")
        histo_img(folder / 'color.png', folder / 'color_histo.jpg')
        histo_img(folder / 'fringe.png', folder / 'fringe_histo.jpg')
        #histo_img(folder / 'nolight.png', folder / 'nolight_histo.jpg')
    if DEVICE_PROCESSING:
        proc_device_data(deviceid, folder)
    if EXPOSURE_PROCESSING:
        Path(folder / 'fringe.png').replace(folder / 'fringe_org.png')
        change_exposure(folder / 'fringe_org.png', folder / 'fringe.png')

    #scan_preprocessing(folder)  # change contrast etc
    general_postprocessing(folder)
    # here the color.png, fringe.png, nolight.png is expected
    if NN_ENABLE:
        process_input_folder(folder)

    
    ply2jpg(folder / 'pointcloud.ply',folder / 'pointcloud_n.jpg',cam='n' )
    if Path.exists(folder / 'pointcloud.jpg'):
        copy2(folder / 'pointcloud.jpg', DEVICE_PATH / deviceid / 'input' / 'last_dias.jpg' )
        copy2(folder / 'pointcloud.jpg', DEVICE_PATH / deviceid / 'input' / 'last_pointcloud.jpg' )

    # filter image
    print ("Filtering")
    #radius_outliersremoval(str(folder / 'pointcloud.ply'),str(folder / 'pointcloud_f1.ply'))
    #ply2jpg(folder / 'pointcloud_f1.ply', folder / 'pointcloud_f1.jpg')



    #scan_filter(folder / 'pointcloud.ply', folder / 'pointcloud_f.ply')
 
    #filter_pcl(folder / 'pointcloud.ply', folder / 'pointcloud1.ply')
    #mask_pcl(folder / 'pointcloud.ply', folder / 'mask.npy', folder / 'nypointcloud.ply')
    #ply2jpg(folder / 'pointcloud1.ply', folder / 'pointcloud1.jpg')
    #ply2jpg(folder / 'nypointcloud.ply', folder / 'nypointcloud.jpg')


def receive_scan(deviceid, folder):
    "Receive scan from device: color.jpg, dias.jpg, nolight.jpg"
    copy2png(folder)
    process_scan(deviceid, folder)
