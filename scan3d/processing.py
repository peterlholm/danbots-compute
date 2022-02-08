"Common NN processing"
# this module is the entrance to the nn processing

from pathlib import Path
from shutil import copy2

#from matplotlib.pyplot import sca
from compute.settings import DEVICE_PATH, GEN_3D_PICTURES, NN_ENABLE
from utils.pcl_utils import ply2jpg
from utils.histoimg import histo_img
#from .nn.inference.config import COLOR_FILENAME, FRINGE_FILENAME, NOLIGHT_FILENAME #, POINTCLOUD_JPG_FILENAME
#from .filtering import radius_outliersremoval, scan_filter

if NN_ENABLE:
    from .nn.inference.process_input import process_input_folder

_DEBUG = False

def _nn_process(folder):
    "receive png files"
    if _DEBUG:
        histo_img(folder / 'color.png', folder / 'color_nn.jpg')
        histo_img(folder / 'fringe.png', folder / 'fringe_nn.jpg')
        #histo_img(folder / 'nolight.png', folder / 'nolight_histo.jpg')
    if NN_ENABLE:
        process_input_folder(folder)

def process(folder):
    if NN_ENABLE:
        _nn_process(folder)
        if GEN_3D_PICTURES:
            ply2jpg(folder / 'pointcloud.ply', folder / 'pointcloud.jpg')
            # ply2jpg(folder / 'pointcloud.ply',folder / 'pointcloud_n.jpg',cam='n' )
            # ply2jpg(folder / 'pointcloud.ply',folder / 'pointcloud_e.jpg',cam='e' )
            # ply2jpg(folder / 'pointcloud.ply',folder / 'pointcloud_w.jpg',cam='w' )
