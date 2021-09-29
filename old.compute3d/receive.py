#
# this module start the processing of the picture received from devices
#
import os
from pathlib import Path
import threading
import datetime
import shutil
from compute.settings import DATA_PATH, NN_ENABLE #, TEMP_PATH
from api.utils import save_uploaded_file
from send2live.send2live import send_picture, send_ply_picture

#from compute3d.nn_process import process_input, test_process_input

INPUT_FOLDER = 'input'
ARCHIVE_FOLDER = 'archive'

ARCHIVE_DATA = True
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

# def save_uploaded_file(handle, filepath):
#     with open(filepath, 'wb+') as destination:
#         for chunk in handle.chunks():
#             destination.write(chunk)

def start_scan(device_path):
    # archive last input folder
    infolder = device_path / INPUT_FOLDER
    os.makedirs(infolder, exist_ok=True)
    if ARCHIVE_DATA:
        if os.path.exists(infolder):
            datestr = datetime.datetime.now().strftime('%y%m%d-%H%M')
            outfolder = device_path / ARCHIVE_FOLDER / datestr
            shutil.copytree(infolder, outfolder, dirs_exist_ok=True)
    # clean folder
    shutil.rmtree(infolder)
    os.makedirs(infolder, exist_ok=True)

#@background
def receive_pic_set(device, set_number, color_picture, dias_picture, noligt_picture):
    print("Picture received device:", device, set_number)
    folder = DATA_PATH / device / 'input' / str(set_number)
    os.makedirs(folder, exist_ok=True)
    save_uploaded_file(color_picture, folder / COLOR_PICTURE )
    save_uploaded_file(dias_picture, folder / DIAS_PICTURE )
    save_uploaded_file(noligt_picture, folder / NOLIGHT_PICTURE )

    if False:
        process_input(folder)

    result = send_picture(device, folder / COLOR_PICTURE )
    if not result:
        print("Send picture failed")
    plyfile = Path(__file__).resolve().parent / 'test.ply'
    #print("plyfile", plyfile)
    # result = send_ply_picture(device, plyfile )
    # if not result:
    #     print("Send ply picture failed")
    return True

def stop_scan(device_path):
    print('Scan Stop device:', device_path)

def test_nn():
    folder = DATA_PATH / 'test/1'
    if NN_ENABLE:
        #result = test_process_input(folder)
        return result
    return {'NeuralNet': False}
