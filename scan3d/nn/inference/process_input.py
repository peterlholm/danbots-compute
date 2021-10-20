"NN processing"
#import os
#from datetime import datetime
#from shutil import copytree, rmtree
from pathlib import Path
#from nn.prepare_input import prepare_blender_input, COLORPICTURE
#from nn.inference.wrap_net import wrap_net
from utils.pcl2jpg import ply2jpg
from utils.pclutils import mirror_pcl
from .config import COLOR_FILENAME, MASK_FILENAME, NOLIGHT_FILENAME, POINTCLOUD_FILENAME
from .create_mask import create_mask
from .H_model import nnHprocess
from .L_model import nnLprocess
from .depth import newDepth
from .pointcloud import nngenerate_pointcloud


_DEBUG=False

def process_input_folder(folder):
    if _DEBUG:
        print("processing folder: ", folder)
    if not Path.exists(folder):
        raise Exception("Input directory does not exist", folder)

    #prepare_blender_input(infolder, outfolder)

    #folder = outfolder
    create_mask(folder / COLOR_FILENAME, folder / NOLIGHT_FILENAME, folder)

    #print(Hmodel)
    nnHprocess(folder)
    nnLprocess(folder)
    newDepth(folder, 300)

    nngenerate_pointcloud(folder / COLOR_FILENAME, folder / MASK_FILENAME, folder / 'nndepth.npy', folder / 'pointcl-nndepth.ply')

    mirror_pcl(folder / POINTCLOUD_FILENAME, folder / 'pointcloud.ply')
    ply2jpg(folder / 'pointcloud.ply', folder / 'pointcloud.jpg')
    if _DEBUG:
        print ("Processing endet")

def process_nn():
    return
    