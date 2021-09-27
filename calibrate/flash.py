"""
flash test
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageStat, ImageFilter # ImageEnhance,
#from configparser import ConfigParser
#from api.views import device_folder
from compute.settings import DATA_PATH
from api.device_config import read_device_config, save_device_config

FOLDER = "calibrate/testdata/"
FILE_NAME = "flash01.jpg"
CALIBRATE_SECTION = 'calibrate'
LED_LIGHT_CORR = 'led_corr.png'
CENTER_AREA = 0.3   # the part to be excluded
COMP_OFFSET = 200

_DEBUG =True

file = Path(FOLDER+FILE_NAME)

def read_config_section(device):
    config = read_device_config(device)
    config = read_device_config('123')
    #print(config.sections())
    if CALIBRATE_SECTION not in config.sections():
        print ("adding section")
        config.add_section(CALIBRATE_SECTION)
    #cal_section = config[CALIBRATE_SECTION]
    # print(cal_section.items())
    # for key in cal_section.items():
    #     print (key)
    return config

def save_config(config):
    save_device_config(config, "123")

def flash_led_test(device="123"):
    device_folder = DATA_PATH / device
    config = read_config_section(device)
    img = Image.open(file)
    grey = img.convert('L')
    grey.show()
    width = img.width
    height = img.height
    # calculate mean from center area
    reduce = 0.30
    rect = (width*reduce/2, height*reduce/2, width*(1-reduce/2), height*(1-reduce/2))
    mask = Image.new('L', img.size, color=0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle(rect,fill=255)
    grey.putalpha(mask)
    mean = int(ImageStat.Stat(grey).mean[0])
    print("mean", mean)
    # restore image
    grey = img.convert('L')
    korr = Image.new('L', grey.size)
    for x in range(0, grey.width):
        for y in range(0, grey.height):
            val = mean - grey.getpixel((x,y)) + COMP_OFFSET
            korr.putpixel((x,y), val )
    #korr.save(devce_folder / LED_LIGHT_CORR)
    medkorr = korr.filter(ImageFilter.MedianFilter(size=31))
    medkorr.show()
    medkorr.save(device_folder / LED_LIGHT_CORR)

    repair = Image.new('L', grey.size)
    for x in range(0, repair.width):
        for y in range(0, repair.height):
            val = grey.getpixel((x,y)) + (medkorr.getpixel((x,y)) - COMP_OFFSET)
            #print(val)
            repair.putpixel((x,y), val )
    repair.show()

    config[CALIBRATE_SECTION]['flash_calibration'] = '1'
    config[CALIBRATE_SECTION]['light_correction'] = LED_LIGHT_CORR
    config[CALIBRATE_SECTION]['light_mask'] = "light_mask.png"
    save_config(config)
    return True
