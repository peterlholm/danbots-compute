"NN processing"
#import os
#from datetime import datetime
#from shutil import copytree, rmtree
from pathlib import Path
from utils.pcl_utils import ply2jpg
from utils.pcl_utils import mirror_pcl, mask_pcl
from utils.show_npy import show_npy
from utils.pic_utils import include_pic_mask
from utils.np_utils import add_0mask_file, add_mask, mask_file
from .config import COLOR_FILENAME, FRINGE_FILENAME, MASK_FILENAME, NOLIGHT_FILENAME, POINTCLOUD_FILENAME
from .create_mask import create_mask, create_nomask, create_0mask
from .H_model import nnHprocess
from .L_model import nnLprocess
from .depth import newDepth
from .pointcloud import nngenerate_pointcloud

_DEBUG=False
_NET2=False

def process_input_folder(folder):
    "Process folder through normal nn processing"
    if _DEBUG:
        print("NN processing folder: ", folder)
    if not Path.exists(folder):
        raise Exception("Input directory does not exist", folder)

    # create mask.npy (and mask.png)
    create_mask(folder / COLOR_FILENAME, folder / NOLIGHT_FILENAME, folder)
    create_0mask(folder / COLOR_FILENAME, folder / NOLIGHT_FILENAME, folder)
    #create_nomask(folder)
    include_pic_mask(folder / FRINGE_FILENAME, folder / 'mask0.png', folder / 'fringe22.png')

    nnHprocess(folder)
    # create nnwrap1.npy and nnwrap1.png from fringe.png

    if _DEBUG:
        print ("creating masked wrap")
    mask_file( folder /'nnwrap1.npy', folder /'mask.npy', folder /'dummy.npy')
    show_npy(folder / 'dummy.npy', folder / "dummy.png", grey=True)

    if _NET2:
        nnLprocess(folder) # generate nnunwrap.png
        show_npy(folder / 'nnunwrap.npy', folder / "test.png")

        newDepth(folder, 30)

        nngenerate_pointcloud(folder / COLOR_FILENAME, folder / MASK_FILENAME, folder / 'nndepth.npy', folder / 'pointcl-nndepth.ply')

        mirror_pcl(folder / POINTCLOUD_FILENAME, folder / 'pointcloud.ply')
        #mask_pcl(folder / 'pointcloud.ply', folder / 'mask.npy', folder / 'nypointcloud.ply')
        ply2jpg(folder / 'pointcloud.ply', folder / 'pointcloud.jpg')
        #ply2jpg(folder / 'nypointcloud.ply', folder / 'nypointcloud.jpg')
        if _DEBUG:
            print ("Processing endet")
