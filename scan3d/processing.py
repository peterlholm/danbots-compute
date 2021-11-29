"Common NN processing"
from pathlib import Path
from shutil import copy2

#from matplotlib.pyplot import sca
from compute.settings import DEVICE_PATH, NN_ENABLE
from utils.pcl_utils import ply2jpg
from utils.histoimg import histo_img
#from .nn.inference.config import COLOR_FILENAME, FRINGE_FILENAME, NOLIGHT_FILENAME #, POINTCLOUD_JPG_FILENAME
#from .filtering import radius_outliersremoval, scan_filter

if NN_ENABLE:
    from .nn.inference.process_input import process_input_folder

_DEBUG = True

def nn_process(folder):
    "receive png files"
    if _DEBUG:
        #print(f"Receiveing scan from {deviceid} in {folder}")
        histo_img(folder / 'color.png', folder / 'color_nn.jpg')
        histo_img(folder / 'fringe.png', folder / 'fringe_nn.jpg')
        #histo_img(folder / 'nolight.png', folder / 'nolight_histo.jpg')
    if NN_ENABLE:
        process_input_folder(folder)

def process(deviceid, folder):
    nn_process(folder)
    if NN_ENABLE:
        # ply2jpg(folder / 'pointcloud.ply',folder / 'pointcloud_n.jpg',cam='n' )
        # ply2jpg(folder / 'pointcloud.ply',folder / 'pointcloud_e.jpg',cam='e' )
        # ply2jpg(folder / 'pointcloud.ply',folder / 'pointcloud_w.jpg',cam='w' )

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
