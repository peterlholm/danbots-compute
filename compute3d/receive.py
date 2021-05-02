#
# this module start the processing of the picture received from devices
#
import os
import threading
import datetime
import shutil
from compute.settings import DATA_PATH #, TEMP_PATH
from send2live.send2live import send_picture #, send_ply_picture
from compute3d.nn_process import process_input

COLOR_PICTURE = 'image8.jpg'
DIAS_PICTURE = 'image0.jpg'
NOLIGHT_PICTURE = 'image9.jpg'

def background(myfunction):
    '''
    a threading decorator
    use @background above the function you want to run in the background
    '''
    def bg_f(*a, **kw):
        print(myfunction.__name__)
        threading.Thread(target=myfunction, name=myfunction.__name__, args=a, kwargs=kw).start()
    return bg_f

def save_uploaded_file(handle, filepath):
    with open(filepath, 'wb+') as destination:
        for chunk in handle.chunks():
            destination.write(chunk)

def start_scan(device):
    print('Scan Start device:', device)
    infolder = DATA_PATH / 'input' / device
    datestr = datetime.datetime.now().isoformat()
    outfolder = DATA_PATH / 'arkiv' / device
    os.makedirs(outfolder, exist_ok=True)
    shutil.move(infolder, outfolder / datestr)

#@background
def receive_pic_set(device, set_number, color_picture, french_picture, noligt_picture):
    print("Picture received device:", device, set_number)
    folder = DATA_PATH / 'input' / device / str(set_number)
    os.makedirs(folder, exist_ok=True)
    save_uploaded_file(color_picture, folder / COLOR_PICTURE )
    save_uploaded_file(french_picture, folder / DIAS_PICTURE )
    save_uploaded_file(noligt_picture, folder / NOLIGHT_PICTURE )

    process_input(folder)

    result = send_picture(device, folder / COLOR_PICTURE )
    if not result:
        print("Send picture failed")
    return True

def stop_scan(device):
    print('Scan Stop device:', device)

def test_nn():
    folder = DATA_PATH / 'test/1'

    process_input(folder)
    