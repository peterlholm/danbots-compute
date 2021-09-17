from os.path import exists
import configparser

CONFIG_FILE = "device_config.conf"

myconfig = configparser.ConfigParser()

def read_config():
    config = configparser.ConfigParser()
    if exists(CONFIG_FILE):
        with open(CONFIG_FILE,'r', encoding="UTF8") as configfile:
            myconfig.read_file(configfile)
        print("reading config")
    return config

def save_config(config):
    with open(CONFIG_FILE, 'w', encoding="UTF8") as configfile:
        config.write(configfile)

myconfig = read_config()
DEVICEID = myconfig.get('device','deviceid',fallback='11223344')

print (DEVICEID)

#print (myconfig)
myconfig['device'] = {"deviceid":"2345"}

save_config(myconfig)
