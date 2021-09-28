import os
from compute.settings import DATA_PATH, NN_ENABLE
from api.utils import save_uploaded_file
from api.device_config import read_config
from nn.inference.config import COLOR_FILENAME, FRINGE_FILENAME, NOLIGHT_FILENAME
if NN_ENABLE:    
    from nn.inference.process_input import process_input_folder

def receive_pic_set(device, set_number, color_picture, dias_picture, noligt_picture):
    print("Picture received device:", device, set_number)
    folder = DATA_PATH / device / 'input' / str(set_number)
    os.makedirs(folder, exist_ok=True)
    save_uploaded_file(color_picture, folder / COLOR_FILENAME )
    save_uploaded_file(dias_picture, folder / FRINGE_FILENAME )
    save_uploaded_file(noligt_picture, folder / NOLIGHT_FILENAME)

    deviceconfig = read_config(DATA_PATH / device)
    print (deviceconfig)

    if NN_ENABLE:
        process_input_folder(folder)

    # result = send_picture(device, folder / COLOR_FILENAME )
    # if not result:
    #     print("Send picture failed")
    # plyfile = Path(__file__).resolve().parent / 'test.ply'
    #print("plyfile", plyfile)
    # result = send_ply_picture(device, plyfile )
    # if not result:
    #     print("Send ply picture failed")
    return True
