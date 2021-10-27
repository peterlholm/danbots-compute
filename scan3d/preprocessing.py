"preprocess before nn"
from pathlib import Path
from scan3d.nn.inference.config import FRINGE_FILENAME
from utils.histoimg import histo_img
from utils.img_utils import change_contrast, change_brightness
#from PIL import Image

def change_exposure(infile, outfile):
    tempfile = "temp.png"
    change_contrast(infile, tempfile, 0.6)
    change_brightness(tempfile, outfile, 1.6)

def preprocessing(folder):
    print("generating histograms")
    #histo_img(folder / 'color.jpg', folder / 'color_histo.jpg')
    histo_img(folder / 'color.png', folder / 'color_histo.png')
    #histo_img(folder / 'fringe.png', folder / 'fringe_histo.png')

    Path(folder / 'fringe.png').rename(folder / 'dev_fringe.png')
    change_exposure(folder / 'dev_fringe.png', folder / 'fringe.png')
    histo_img(folder / 'fringe.png', folder / 'fringe_new_histo.png')


def dummy(folder):
    change_contrast(folder / FRINGE_FILENAME, folder /"contrast.png", 0.5)
    histo_img(folder / 'contrast.png', folder / 'contrast_histo.png')

    change_brightness(folder / 'contrast.png', folder /"bright.png", 1.5)
    histo_img(folder / 'bright.png', folder / 'bright_histo.png')

    change_brightness(folder / FRINGE_FILENAME, folder /"bright2.png", 1.6)
    histo_img(folder / 'bright2.png', folder / 'bright2_histo.png')

    change_contrast(folder / 'bright2.png', folder /"contrast2.png", 0.8)
    histo_img(folder / 'contrast2.png', folder / 'contrast2_histo.png')
