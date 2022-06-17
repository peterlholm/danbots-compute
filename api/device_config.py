"""
get device config information
"""
from os.path import exists
from pathlib import Path
import configparser
from compute.settings import DATA_PATH

CONFIG_FILE = "device_config.conf"
_DEBUG = False

myconfig = configparser.ConfigParser()

def _read_config(folder):
    "read and parse config from device folder"
    #config = configparser.ConfigParser()
    config_file = folder / CONFIG_FILE
    if exists(config_file):
        with open(config_file,'r', encoding="UTF8") as configfile:
            myconfig.read_file(configfile)
        #print("reading config")
    else:
        if _DEBUG:
            print("no config file", folder)
    return myconfig

def _save_config(config, folder):
    "save the device configuration in folder"
    config_file = folder / CONFIG_FILE
    with open(config_file, 'w', encoding="UTF8") as configfile:
        config.write(configfile)

def read_device_config(device):
    "read config for device"
    config_folder = DATA_PATH / "device" /device
    #print(config_folder)
    return _read_config(config_folder)

def save_device_config(config, device):
    "save config for device"
    config_folder = DATA_PATH / "device" / device
    Path(config_folder).mkdir(parents=True, exist_ok=True)
    return _save_config(config, config_folder)
