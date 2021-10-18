from shutil import copy2
from compute.settings import DEVICE_PATH
_DEBUG = True

def receive_scan(deviceid, folder):
    print(f"Receiveing scan from {deviceid} in {folder}")
    # copy file
    copy2(folder / 'dias.jpg', DEVICE_PATH / deviceid / 'last_dias.jpg' )
    #save_uploaded_file(j, devicefolder / 'input' / 'last_dias.jpg')
