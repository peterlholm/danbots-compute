import os
from datetime import datetime
from shutil import copytree, rmtree
from pathlib import Path
from nn.inference.prepare_input import prepare_blender_input
#from nn.inference.wrap_net import wrap_net
from nn.inference.config import COLOR_FILENAME, NOLIGHT_FILENAME
from nn.inference.create_mask import create_mask
from nn.inference.H_model import Hmodel, nnHprocess
from nn.inference.L_model import nnLprocess
from nn.inference.depth import newDepth

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

    print(Hmodel)
    nnHprocess(folder)
    nnLprocess(folder)
    newDepth(folder, 300)

    #nngenerate_pointcloud(folder+str(i) +'/'+ 'image8.png', folder+str(i) +'/'+ 'mask.png', folder+str(i)+'/' + 'nndepth.npy', folder+str(i)+'/' +'pointcl-nndepth.ply')

    print ("Processing endet")
    return

def process_nn():
    return
    