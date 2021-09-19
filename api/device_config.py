from os.path import exists
import configparser

CONFIG_FILE = "device_config.conf"

myconfig = configparser.ConfigParser()

def read_config(folder):
    config = configparser.ConfigParser()
    config_file = folder / CONFIG_FILE
    if exists(config_file):
        with open(config_file,'r', encoding="UTF8") as configfile:
            myconfig.read_file(configfile)
        print("reading config")
    return config

def save_config(config, folder):
    config_file = folder / CONFIG_FILE
    with open(config_file, 'w', encoding="UTF8") as configfile:
        config.write(configfile)

# myconfig = read_config()
# DEVICEID = myconfig.get('device','deviceid',fallback='11223344')

# print (DEVICEID)

# #print (myconfig)
# myconfig['device'] = {"deviceid":"2345"}

# save_config(myconfig)
