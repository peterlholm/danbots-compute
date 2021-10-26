import os
from datetime import datetime
from shutil import copytree, rmtree
from pathlib import Path
from .prepare_input import prepare_blender_input, COLORPICTURE
#from nn.inference.wrap_net import wrap_net
from config import COLOR_FILENAME, NOLIGHT_FILENAME
from create_mask import create_mask
from H_model import Hmodel, nnHprocess
from L_model import nnLprocess
from depth import newDepth
from pointcloud import nngenerate_pointcloud
from utils.pcl2png import pcl2png

def process_blender_folder(infolder, outfolder):
    # receive a folder from blender, convert to standard files
    # pass standard files through wrap_net and k_net

    print("processing folder: ", infolder)
    if not Path.exists(infolder):
        raise Exception("Input directory does not exist", infolder)
        return False

    prepare_blender_input(infolder, outfolder)
    
    folder = outfolder
    create_mask(folder / COLOR_FILENAME, folder / NOLIGHT_FILENAME, folder)

    #print(Hmodel)
    nnHprocess(folder)
    nnLprocess(folder)
    #newDepth(folder, 300)

    nngenerate_pointcloud(folder / COLOR_FILENAME, folder /'mask.png', folder / 'nndepth.npy', folder / 'pointcl-nndepth.ply')

    pcl2png(folder / 'pointcl-nndepth.ply',folder / 'pointcl-nndepth.png')
    print ("Processing endet")
    return

def process_nn_folder(folder):
    create_mask(folder / COLOR_FILENAME, folder / NOLIGHT_FILENAME, folder)

    nnHprocess(folder)
    nnLprocess(folder)
    newDepth(folder, 30)

    nngenerate_pointcloud(folder / COLOR_FILENAME, folder /'mask.png', folder / 'nndepth.npy', folder / 'pointcl-nndepth.ply')

    pcl2png(folder / 'pointcl-nndepth.ply',folder / 'pointcl-nndepth.png')

    print ("Processing endet")



def process_nn():
    return
    