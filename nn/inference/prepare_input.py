from pathlib import Path
from PIL import Image

COLORPICTURE = "image8.png"
BLACKWHITEPICTURE = "image8.png"
DIASPICTURE = "image0.png"
NOLIGHT = "image9.png"

OUTCOLOR = "color.png"
OUTDIAS = "dias.png"
OUTNOLIGHT = "nolight.png"

def prepare_blender_input(infolder, outfolder=None):
    if not outfolder:
        outfolder = infolder
    pic = Image.open(infolder / COLORPICTURE)
    pic.save(Path(outfolder) / OUTCOLOR)
    pic = Image.open(infolder / DIASPICTURE)
    pic.save(Path(outfolder) / OUTDIAS)
    pic = Image.open(infolder / NOLIGHT)
    pic.save(Path(outfolder) / OUTNOLIGHT)
    return
