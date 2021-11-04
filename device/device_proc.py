"""
Process date acoording to device parameters
"""
from os import read
from api.device_config import read_device_config, save_device_config
from scan3d.nn.inference.config import FRINGE_FILENAME
from utils.img_utils import rotate_img
from utils.pic_utils import insert_mask
from utils.histoimg import histo_img, get_mask

_DEBUG=False

def rotation(config, infile, outfile):
    #config = read_device_config(device)
    slope = float(config['calibrate']['slope'])
    print("slope", slope)
    rotate_img(infile, -slope*30.0, outfile)

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
        if False:
            rotation(config,folder / 'dias.jpg', folder / 'fringe.png')
            # slope = float(config['calibrate']['slope'])
            # print("slope", slope)
            # rotate_img(folder / 'dias.jpg', -slope*30.0, folder / 'fringe.png')
        if True:
            if _DEBUG:
                print("create device masks")
            picture_mask(config, folder / 'color.jpg', folder / 'color.png')
            picture_mask(config, folder / 'nolight.jpg', folder / 'nolight.png')
            dias_mask(config, folder / 'dias.jpg', folder / 'fringe.png')
            #mymask = get_mask(folder / 'fringe.png')  
            #mymask.show()
            #histo_img(folder / 'color.jpg', folder / 'mycolor_histo.png')
            if _DEBUG:
                histo_img(folder / 'fringe.png', folder / 'device_fringe_histo.png')
            #histo_img(folder / 'dias.png', folder / 'mydias_histo2.png', mask=mymask)
    if _DEBUG:
        print("finish proc_device_data")
    return True

