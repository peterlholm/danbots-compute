import os
from datetime import datetime
from shutil import copytree, rmtree
from pathlib import Path
from nn.inference.prepare_input import prepare_blender_input
from nn.inference.wrap_net import process_net

def process_data(infolder):
    tmpfolder = "tmp"
    print("processing folder: ", infolder)
    if not Path.exists(infolder):
        print ("Input directory does not exist: " + str(infolder))
        raise Exception("Input directory does not exist", infolder)
        return False
# clean folder
    rmtree(tmpfolder)
    os.makedirs(tmpfolder, exist_ok=True)
    prepare_blender_input(infolder, tmpfolder)
    process_net(tmpfolder)
    #k_net(folder)

    print ("Processing endet")
    return
