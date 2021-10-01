import os
from datetime import datetime
from shutil import copytree, rmtree
from pathlib import Path
from nn.prepare_input import prepare_blender_input, COLORPICTURE
#from nn.inference.wrap_net import wrap_net
from nn.inference.config import COLOR_FILENAME, MASK_FILENAME, NOLIGHT_FILENAME
from nn.inference.create_mask import create_mask
from nn.inference.H_model import Hmodel, nnHprocess
from nn.inference.L_model import nnLprocess
from nn.inference.depth import newDepth
from nn.inference.pointcloud import nngenerate_pointcloud
from Utils.Imaging.pcl2png import pcl2png

def process_input_folder(folder):
    print("processing folder: ", folder)
    if not Path.exists(folder):
        raise Exception("Input directory does not exist", folder)
        return False

    #prepare_blender_input(infolder, outfolder)
    
    #folder = outfolder
    create_mask(folder / COLOR_FILENAME, folder / NOLIGHT_FILENAME, folder)

    #print(Hmodel)
    nnHprocess(folder)
    nnLprocess(folder)
    newDepth(folder, 300)

    nngenerate_pointcloud(folder / COLOR_FILENAME, folder / MASK_FILENAME, folder / 'nndepth.npy', folder / 'pointcl-nndepth.ply')

    pcl2png(folder / 'pointcl-nndepth.ply',folder / 'pointcl-nndepth.png')

    print ("Processing endet")
    return

def process_nn():
    return
    