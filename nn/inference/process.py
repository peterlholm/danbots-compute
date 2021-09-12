import os
from datetime import datetime
from shutil import copytree, rmtree
from pathlib import Path
from nn.inference.prepare_input import prepare_blender_input
from nn.inference.wrap_net import process_net

def process_blender_folder(infolder, outfolder):
    # receive a folder from blender, convert to standard files
    # pass standard files through wrap_net and k_net

    #tmpfolder = "tmp"
    print("processing folder: ", infolder)
    if not Path.exists(infolder):
        raise Exception("Input directory does not exist", infolder)
        return False

    #rmtree(tmpfolder)
    #os.makedirs(tmpfolder, exist_ok=True)
    prepare_blender_input(infolder, outfolder)
    process_net(outfolder)
    #k_net(folder)

    print ("Processing endet")
    return

def process_nn():
    return
    