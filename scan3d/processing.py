"Common processing"
from pathlib import Path
from shutil import copy2, rmtree
#from compute.settings import TEMP_PATH
#from scan3d.nn.inference.config import FRINGE_FILENAME
from utils.histoimg import histo_img
from utils.img_utils import change_contrast, change_brightness
#from PIL import Image

_DEBUG=False

def copy_x_test_set(folder):
    path1 = folder / '1'
    for i in range(2,6):
        newpath = folder / str(i)
        rmtree(newpath, ignore_errors=True)
        Path(newpath).mkdir()
        copy2(path1 / 'color.jpg', newpath / 'color.jpg')
        #copy2(path1 / 'dias.jpg', newpath / 'dias.jpg')
        copy2(path1 / 'nolight.jpg', newpath / 'nolight.jpg')
    change_contrast(folder / '1' / 'dias.jpg', folder / '2' / 'dias.jpg', 0.8)
    change_contrast(folder / '1' / 'dias.jpg', folder / '3' / 'dias.jpg', 1.2)
    change_brightness(folder / '1' / 'dias.jpg', folder / '4' / 'dias.jpg', 0.8)
    change_brightness(folder / '1' / 'dias.jpg', folder / '5' / 'dias.jpg', 1.2)

def copy_test_set(folder):
    path1 = folder / '1'
    for i in range(2,6):
        newpath = folder / str(i)
        rmtree(newpath, ignore_errors=True)
        Path(newpath).mkdir()
        copy2(path1 / 'fringe.png', newpath / 'fringe.png')
        copy2(path1 / 'color.png', newpath / 'color.png')
        copy2(path1 / 'nolight.png', newpath / 'nolight.png')
    change_contrast(folder / '1' / 'fringe.png', folder / '2' / 'fringe.png', 0.8)
    change_contrast(folder / '1' / 'fringe.png', folder / '3' / 'fringe.png', 1.2)
    change_brightness(folder / '1' / 'fringe.png', folder / '4' / 'fringe.png', 0.8)
    change_brightness(folder / '1' / 'fringe.png', folder / '5' / 'fringe.png', 1.2)

def change_exposure(infile, outfile):
    tempfile = Path(outfile).parent / "temp.png"
    change_contrast(infile, tempfile, 0.9)
    change_brightness(tempfile, outfile, 1)

def scan_preprocessing(folder):
    "input fringe.png"
    if _DEBUG:
        print("generating histograms", folder)
        #histo_img(folder / 'color.jpg', folder / 'color_histo.jpg')
        #histo_img(folder / 'color.png', folder / 'color_histo.png')
        #histo_img(folder / 'fringe.png', folder / 'fringe_histo.png')

    Path(folder / 'fringe.png').replace(folder / 'fringe0.png')
    change_exposure(folder / 'fringe0.png', folder / 'fringe.png')
    #histo_img(folder / 'fringe.png', folder / 'fringe_new_histo.png')

def general_postprocessing(folder):
    "preproccsing for scan and blender"
    if _DEBUG:
        histo_img(folder / 'color.png', folder / 'color_histo.png')
        histo_img(folder / 'fringe.png', folder / 'fringe_histo.png')
        #histo_img(folder / 'nolight.png', folder / 'nolight_histo.png')
