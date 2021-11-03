"Receive a blender dataset and prepare it for NN"
from pathlib import Path
#from shutil import copy2
from PIL import Image
from compute.settings import NN_ENABLE
from scan3d.nn.inference.config import COLOR_FILENAME,FRINGE_FILENAME,NOLIGHT_FILENAME
from .preprocessing import general_postprocessing
if NN_ENABLE:
    from scan3d.nn.inference.process_input import process_input_folder

# blender names

COLORPICTURE = "image8.png"
BLACKWHITEPICTURE = "image8.png"
DIASPICTURE = "image0.png"
NOLIGHT = "image9.png"

# OUTCOLOR = "color.png"
# OUTDIAS = "dias.png"
# OUTNOLIGHT = "nolight.png"

_DEBUG = False

def prepare_blender_input(infolder, outfolder=None):
    if not outfolder:
        outfolder = infolder
    pic = Image.open(infolder / COLORPICTURE)
    pic.save(Path(outfolder) / COLOR_FILENAME)
    pic = Image.open(infolder / DIASPICTURE)
    pic.save(Path(outfolder) / FRINGE_FILENAME)
    pic = Image.open(infolder / NOLIGHT)
    pic.save(Path(outfolder) / NOLIGHT_FILENAME)

def receive_scan_set(folder):
    if _DEBUG:
        print("Receive Blender Scan_set", folder)
    general_postprocessing(folder)
    if NN_ENABLE:
        process_input_folder(folder)
