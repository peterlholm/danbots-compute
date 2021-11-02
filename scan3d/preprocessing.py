"preprocess before nn"
from pathlib import Path
from shutil import copy2
from scan3d.nn.inference.config import FRINGE_FILENAME
from utils.histoimg import histo_img
from utils.img_utils import change_contrast, change_brightness
#from PIL import Image

_DEBUG=True

def copy_test_set(folder):
    path1 = folder / '1'
    #print(path1)
    for i in range(2,6):
        newpath = folder / str(i)
        #print(newpath)
        Path(newpath).mkdir()
        copy2(path1 / 'color.jpg', newpath / 'color.jpg')
        #copy2(path1 / 'dias.jpg', newpath / 'dias.jpg')
        copy2(path1 / 'nolight.jpg', newpath / 'nolight.jpg')
    change_contrast(folder / '1' / 'dias.jpg', folder / '2' / 'dias.jpg', 0.8)
    change_contrast(folder / '1' / 'dias.jpg', folder / '3' / 'dias.jpg', 1.2)
    change_brightness(folder / '1' / 'dias.jpg', folder / '4' / 'dias.jpg', 0.9)
    change_brightness(folder / '1' / 'dias.jpg', folder / '5' / 'dias.jpg', 1.1)

def change_exposure(infile, outfile):
    tempfile = "temp.png"
    change_contrast(infile, tempfile, 0.9)
    change_brightness(tempfile, outfile, 0.9)

def scan_preprocessing(folder):
    "input fringe.png"
    if _DEBUG:
        print("generating histograms", folder)
        #histo_img(folder / 'color.jpg', folder / 'color_histo.jpg')
        #histo_img(folder / 'color.png', folder / 'color_histo.png')
        #histo_img(folder / 'fringe.png', folder / 'fringe_histo.png')

    Path(folder / 'fringe.png').replace(folder / 'pre_fringe.png')
    change_exposure(folder / 'pre_fringe.png', folder / 'fringe.png')
    #histo_img(folder / 'fringe.png', folder / 'fringe_new_histo.png')

def general_postprocessing(folder):
    "preproccsing for scan and blender"
    if _DEBUG:
        histo_img(folder / 'color.png', folder / 'color_histo.png')
        histo_img(folder / 'fringe.png', folder / 'fringe_histo.png')
        #histo_img(folder / 'nolight.png', folder / 'nolight_histo.png')

def dummy(folder):
    change_contrast(folder / FRINGE_FILENAME, folder /"contrast.png", 0.5)
    histo_img(folder / 'contrast.png', folder / 'contrast_histo.png')

    change_brightness(folder / 'contrast.png', folder /"bright.png", 1.5)
    histo_img(folder / 'bright.png', folder / 'bright_histo.png')

    change_brightness(folder / FRINGE_FILENAME, folder /"bright2.png", 1.6)
    histo_img(folder / 'bright2.png', folder / 'bright2_histo.png')

    change_contrast(folder / 'bright2.png', folder /"contrast2.png", 0.8)
    histo_img(folder / 'contrast2.png', folder / 'contrast2_histo.png')
