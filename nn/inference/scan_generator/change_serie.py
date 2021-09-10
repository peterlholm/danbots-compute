import os
from pathlib import Path
from PIL import Image, ImageEnhance
from traverse import traverse_serie, gen_serie

COLOR = "color.png"
DIAS = "dias.png"
NOLIGHT = "nolight.png"

def change_contrast(infile, outfile, val):
    # reduse contrast in picture
    img = Image.open(infile)
    enhanger = ImageEnhance.Contrast(img)
    out = enhanger.enhance(val)
    out.save(outfile) 
    return

def change_brightness(infile, outfile, val):
    # reduse contrast in picture
    img = Image.open(infile)
    enhanger = ImageEnhance.Brightness(img)
    out = enhanger.enhance(val)
    out.save(outfile) 
    return

def change_sharpness(infile, outfile, val):
    img = Image.open(infile)
    enhanger = ImageEnhance.Sharpness(img)
    out = enhanger.enhance(val)
    out.save(outfile) 
    return

def copy_pic(infile, outfile):
    img = Image.open(infile)
    img.save(outfile) 
    return

x
def picset_contrast(infolder, outfolder, no):
    for fil in [COLOR, DIAS, NOLIGHT]:
        inpath = infolder / fil
        outpath = outfolder / fil
        change_contrast(inpath, outpath, no/10)
        
def picset_brightness(infolder, outfolder, no):
    for fil in [COLOR, DIAS, NOLIGHT]:
        inpath = infolder / fil
        outpath = outfolder / fil
        change_brightness(inpath, outpath, no/10)

def picset_sharpness(infolder, outfolder, no):
    for fil in [COLOR, DIAS, NOLIGHT]:
        inpath = infolder / fil
        outpath = outfolder / fil
        change_sharpness(inpath, outpath, no/10)

#nfolder = Path('C:\\Peter\\danbots\\pictures\\blender\\bridge1scans')
infolder = Path('original\\0')
outfolder = 'pic\\test2'

gen_serie(infolder, 'pic\\contrast', picset_contrast)
gen_serie(infolder, 'pic\\brightness', picset_brightness)
gen_serie(infolder, 'pic\\sharpness', picset_sharpness)

