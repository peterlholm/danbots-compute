"Receive a blender dataset and prepare it for NN"
from pathlib import Path
from shutil import copy2
from PIL import Image
#from utils.img_utils import change_contrast_brightness
from scan3d.nn.inference.config import COLOR_FILENAME,FRINGE_FILENAME,NOLIGHT_FILENAME
from .processing import process

# blender names

COLORPICTURE = "image8.png"
BLACKWHITEPICTURE = "image8.png"
DIASPICTURE = "image0.png"
NOLIGHT = "image9.png"

# OUTCOLOR = "color.png"
# OUTDIAS = "dias.png"
# OUTNOLIGHT = "nolight.png"

_DEBUG = False

def prepare_blender_input2(infolder, outfolder=None):
    if not outfolder:
        outfolder = infolder
    pic = Image.open(infolder / COLORPICTURE)
    pic.save(Path(outfolder) / COLOR_FILENAME)
    pic = Image.open(infolder / DIASPICTURE)
    pic.save(Path(outfolder) / FRINGE_FILENAME)
    pic = Image.open(infolder / NOLIGHT)
    pic.save(Path(outfolder) / NOLIGHT_FILENAME)

def prepare_blender_input(infolder, outfolder=None):
    if not outfolder:
        outfolder = infolder
    copy2(infolder / COLORPICTURE, outfolder / COLOR_FILENAME )
    copy2(infolder / DIASPICTURE, outfolder / FRINGE_FILENAME )
    copy2(infolder / NOLIGHT, outfolder / NOLIGHT_FILENAME )

def receive_blender_set(infolder, folder):
    if _DEBUG:
        print("Receive Blender Scan_set", folder)
    prepare_blender_input(infolder, folder)
    process_blender(folder)

CONTRAST = 2.1
BRIGHTNESS = 0.9

def process_blender(folder):
    #Path(folder / FRINGE_FILENAME ).replace(folder / 'fringe_org.png')
    #change_contrast_brightness(folder / 'fringe_org.png', folder / FRINGE_FILENAME, contrast=CONTRAST, brightness=BRIGHTNESS)
    process( folder)
