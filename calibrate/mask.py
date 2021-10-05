"""Find mask for picture"""
from pathlib import Path
from PIL import Image, ImageStat, ImageFilter #, ImageEnhance, ImageDraw,
from api.device_config import read_device_config, save_device_config

CALIBRATE_SECTION = 'calibrate'

def create_mask(pathname, blur=False, tolerence=0.85):
    color = Image.open(pathname)
    if blur:
        grey = color.convert('L')
        #img = grey.filter(ImageFilter.MedianFilter(size=50))
        img = grey.filter(ImageFilter.BoxBlur(100))
        #img.show()
    else:
        img = color.convert('L')
    stat = ImageStat.Stat(img)
    mean = stat.mean[0]
    # top
    x = img.width/2
    for y in range(int(img.height*0.2)):
        val = img.getpixel((x,y))
        if val > mean*tolerence:
            break
    top = y
    #bottom
    for y in range(img.height-1, int(img.height*0.8), -1):
        val = img.getpixel((x,y))
        if val > mean*tolerence:
            break
    button = y
    #left
    y = img.height/2
    for x in range(int(img.width*0.2)):
        val = img.getpixel((x,y))
        if val > mean*tolerence:
            break
    left = x
    for x in range(img.width-1, int(img.width*0.8), -1):
        val = img.getpixel((x,y))
        if val > mean*tolerence:
            break
    right = x
    return (left, top, right, button)

def save_flash_mask(device, mask):
    config = read_device_config(device)
    if CALIBRATE_SECTION not in config.sections():
        config.add_section(CALIBRATE_SECTION)
    config[CALIBRATE_SECTION]['flash_mask_left'] = str(mask[0])
    config[CALIBRATE_SECTION]['flash_mask_top'] = str(mask[1])
    config[CALIBRATE_SECTION]['flash_mask_right'] = str(mask[2])
    config[CALIBRATE_SECTION]['flash_mask_bottom'] = str(mask[3])
    save_device_config(config, device)

def save_dias_mask(device, mask):
    config = read_device_config(device)
    if CALIBRATE_SECTION not in config.sections():
        config.add_section(CALIBRATE_SECTION)
    config[CALIBRATE_SECTION]['dias_mask_left'] = str(mask[0])
    config[CALIBRATE_SECTION]['dias_mask_top'] = str(mask[1])
    config[CALIBRATE_SECTION]['dias_mask_right'] = str(mask[2])
    config[CALIBRATE_SECTION]['dias_mask_bottom'] = str(mask[3])
    # calculate dias 160 masks
    faktor = 1944 / 160
    if mask[0] < (8189-1941)/2:
        left = 0
    else:
        left = int((mask[0]-(8189-1941)/2)/faktor)
    if mask[2] > 8189-(8189-1941)/2:
        right = 160
    else:
        right = int(160- (8189-(8189-1941)/2 -mask[2])/faktor )
    config[CALIBRATE_SECTION]['dias_160_left'] = str(left)
    config[CALIBRATE_SECTION]['dias_160_top'] = str(int(mask[1]/faktor))
    config[CALIBRATE_SECTION]['dias_160_right'] = str(right)
    config[CALIBRATE_SECTION]['dias_160_bottom'] = str(int(mask[3]/faktor))
    save_device_config(config, device)

if __name__ == "__main__":
    FILE = "data/device/b827eb05abc2/calibrate/calcamera/flash.jpg"
    mymask = create_mask(Path(FILE))
    print (mymask)
    save_flash_mask("123", mymask)
