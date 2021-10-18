"""
Prepare input to std from blender and device
"""

from pathlib import Path
from shutil import copyfile
from PIL import Image
from nn.inference.config import COLOR_FILENAME, FRINGE_FILENAME,NOLIGHT_FILENAME

COLORPICTURE = "image8.png"
BLACKWHITEPICTURE = "image8.png"
DIASPICTURE = "image0.png"
NOLIGHT = "image9.png"

# OUTCOLOR = "color.png"
# OUTDIAS = "dias.png"
# OUTNOLIGHT = "nolight.png"

def prepare_blender_input(infolder, outfolder=None):
    if not outfolder:
        outfolder = infolder
    pic = Image.open(infolder / COLORPICTURE)
    pic.save(Path(outfolder) / COLOR_FILENAME)
    pic = Image.open(infolder / DIASPICTURE)
    pic.save(Path(outfolder) / FRINGE_FILENAME)
    pic = Image.open(infolder / NOLIGHT)
    pic.save(Path(outfolder) / NOLIGHT_FILENAME)

def prepare_device_input(infolder, outfolder=None):
    if not outfolder:
        outfolder = infolder
    copyfile(infolder / 'color.jpg', outfolder / 'color.jpg')
    copyfile(infolder / 'fringe.jpg', outfolder / 'fringe.jpg')
    copyfile(infolder / 'nolight.jpg', outfolder / 'nolight.jpg')
    pic = Image.open(infolder / 'color.jpg')
    pic.save(Path(outfolder) / COLOR_FILENAME)
    pic = Image.open(infolder / 'fringe.jpg')
    pic.save(Path(outfolder) / FRINGE_FILENAME)
    pic = Image.open(infolder / 'nolight.jpg')
    pic.save(Path(outfolder) / NOLIGHT_FILENAME)
