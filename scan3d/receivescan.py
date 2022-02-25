"Receive a scanner data set do device preprocessing and prepare it for NN"
from pathlib import Path
from shutil import copy2

#from matplotlib.pyplot import sca
from compute.settings import DEVICE_PATH, NN_ENABLE, GEN_3D_PICTURES #, NN_ENABLE
from device.device_proc import proc_device_data
#from scan3d.nn.inference.nn_util import make_grayscale
from utils.img2img import img2img
from utils.img_utils import  change_brightness_contrast, convert_green_to_grey #, change_contrast_brightness,change_brightness, change_contrast, convert_to_grey, make_grayscale2
from utils.pcl_utils import ply2jpg, filter_pcl
from utils.histoimg import histo_img
#from utils.np_utils import multiply
from .nn.inference.config import COLOR_FILENAME, NOLIGHT_FILENAME #, FRINGE_FILENAME #, POINTCLOUD_JPG_FILENAME
#from .test_set import general_postprocessing
#from .filtering import radius_outliersremoval, scan_filter
from .processing import process

# if NN_ENABLE:
#     from .nn.inference.process_input import process_input_folder

_DEBUG = False
DEVICE_PROCESSING = True
EXPOSURE_PROCESSING = True
CONTRAST = 1.1
BRIGHTNESS = 0.9

def copy2png(folder):
    img2img(folder / 'color.jpg', folder / COLOR_FILENAME)
    img2img(folder / 'dias.jpg', folder / 'dias.png')
    img2img(folder / 'nolight.jpg', folder / NOLIGHT_FILENAME)

def change_exposure(infile, outfile, contrast=CONTRAST, brightness=BRIGHTNESS):
    #change_brightness(infile, 'dark.png', brightness)
    #histo_img('dark.png', 'dark_histo.jpg', title="dark")
    #change_contrast(infile, outfile, contrast)
    #change_contrast_brightness(infile, outfile, contrast=contrast, brightness=brightness)
    change_brightness_contrast(infile, outfile, contrast=contrast, brightness=brightness)
    #multiply(outfile, outfile, 1.2)

def process_scan(deviceid, folder):
    "receive png files  dias, color, nolight"
    if _DEBUG:
        #print(f"Receiveing scan from {deviceid} in {folder}")
        histo_img(folder / 'color.png', folder / 'color_histo.jpg', title="Org color input")
        histo_img(folder / 'dias.png', folder / 'dias_histo.jpg', title="Org dias input")
        #histo_img(folder / 'nolight.png', folder / 'nolight_histo.jpg')
    if DEVICE_PROCESSING:
        proc_device_data(deviceid, folder)
    if EXPOSURE_PROCESSING:
        # make_grayscale2(folder / 'fringe.png', folder / 'grey1.png')
        # convert_to_grey(folder / 'fringe.png', folder / 'grey2.png')
        # histo_img(folder / 'grey1.png', folder / 'grey_histo.jpg', title="Grey dias input")

        Path(folder / 'dias.png').replace(folder / 'dias_org.png')
        change_exposure(folder / 'dias_org.png', folder / 'dias.png')

        convert_green_to_grey(folder / 'dias.png', folder / 'fringe.png')
        histo_img(folder / 'fringe.png', folder / 'fringe_histo.jpg', title="Green fringe input")

        # histo_img(folder / 'fringe.png', folder / 'fringe_histo2.jpg', title="Fringe after change exposure")
        # convert_green_to_grey(folder / 'fringe.png', folder / 'green.png')
        # histo_img(folder / 'green.png', folder / 'green_histo.jpg', title="Green dias input")
    else:
        copy2(folder / 'dias.png', folder / 'fringe.png')

    #scan_preprocessing(folder)  # change contrast etc
    #general_postprocessing(folder)

    # here the color.png, fringe.png, nolight.png is expected
    process(folder)

    # filter
    if NN_ENABLE:
        if _DEBUG:
            print ("Filtering Scan")

        filter_pcl(folder / 'pointcloud.ply', folder / 'pointcloud_f.ply')
        if GEN_3D_PICTURES:
            pass
            #ply2jpg(folder / 'pointcloud_f.ply',folder / 'pointcloud_f.jpg' )
            #ply2jpg(folder / 'pointcloud.ply',folder / 'pointcloud_n.jpg' )
        if Path.exists(folder / 'pointcloud.jpg'):
            copy2(folder / 'pointcloud.jpg', DEVICE_PATH / deviceid / 'input' / 'last_picture.jpg' )
            copy2(folder / 'pointcloud.jpg', DEVICE_PATH / deviceid / 'input' / 'last_pointcloud.jpg' )

        #radius_outliersremoval(str(folder / 'pointcloud.ply'),str(folder / 'pointcloud_f1.ply'))
        #ply2jpg(folder / 'pointcloud_f1.ply', folder / 'pointcloud_f1.jpg')

        #scan_filter(folder / 'pointcloud.ply', folder / 'pointcloud_f.ply')

        #filter_pcl(folder / 'pointcloud.ply', folder / 'pointcloud1.ply')
        #mask_pcl(folder / 'pointcloud.ply', folder / 'mask.npy', folder / 'nypointcloud.ply')
        #ply2jpg(folder / 'pointcloud1.ply', folder / 'pointcloud1.jpg')
        #ply2jpg(folder / 'nypointcloud.ply', folder / 'nypointcloud.jpg')
    else:
        copy2(folder / 'dias.png', DEVICE_PATH / deviceid / 'input' / 'last_picture.jpg' )

def receive_scan(deviceid, folder):
    "Receive scan from device (api): color.jpg, dias.jpg, nolight.jpg"
    copy2png(folder)
    process_scan(deviceid, folder)
