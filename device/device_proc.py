"""
Process date acoording to device parameters
"""
from os import read
from api.device_config import read_device_config, save_device_config
from scan3d.nn.inference.config import FRINGE_FILENAME
from utils.img_utils import rotate_img
from utils.mask_utils import convert_mask_to_color, insert_mask
from utils.histoimg import histo_img, get_mask

_DEBUG=True

def rotation(config, infile, outfile):
    print(infile, outfile)
    #config = read_device_config(device)
    slope = float(config['calibrate']['slope'])
    print("slope", slope)
    rotate_img(infile, -slope, outfile)

def mask(mask, infile, outfile):
    insert_mask(infile, mask, outfile)
    return

def picture_mask(config, infile, outfile):
    "insert device mask in picture"
    top = config['calibrate'].getint("flash_mask_top",0)
    left = config['calibrate'].getint("flash_mask_left",0)
    right = config['calibrate'].getint("flash_mask_right",159)
    bottom = config['calibrate'].getint("flash_mask_bottom",159)
    pic_mask = (top,left,right,bottom)
    #print("pic_mask", pic_mask)
    mask(pic_mask, infile, outfile)
    return

def dias_mask(config, infile, outfile):
    "insert device mask in picture"
    top = config['calibrate'].getint("dias_mask_top",0)
    left = config['calibrate'].getint("dias_mask_left",0)
    right = config['calibrate'].getint("dias_mask_right",159)
    bottom = config['calibrate'].getint("dias_mask_bottom",159)
    pic_mask = (top,left,right,bottom)
    #print("pic_mask", pic_mask)
    mask(pic_mask, infile, outfile)
    return

def proc_device_data(device, folder):
    if _DEBUG:
        print(f"Device specifix processing, device: {device} folder: {folder}")
        print("Overwriting color.png and fringe.png")
    config = read_device_config(device)
    if config.has_section('calibrate'):
        #print("calibrate section exist")
        # rotation
        if True:
            if _DEBUG:
                print("apply rotation")
                rotation(config,folder / 'dias.png', folder / 'dias.png')
        # masks
        if True:
            if _DEBUG:
                print("Apply device masks")
            picture_mask(config, folder / 'color.png', folder / 'color.png')
            picture_mask(config, folder / 'nolight.png', folder / 'nolight.png')
            dias_mask(config, folder / 'dias.png', folder / 'dias.png')
            #histo_img(folder / 'color.jpg', folder / 'mycolor_histo.png')
            if _DEBUG:
                histo_img(folder / 'dias.png', folder / 'device_fringe_histo.png')
    if _DEBUG:
        print("finish proc_device_data")
    return True

