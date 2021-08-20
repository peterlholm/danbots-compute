#
# this module send results to API/Live server
#
from sys import platform
import os.path
import requests
from compute.settings import API_SERVER #, DATA_PATH,TEMP_PATH

PIC2D_FUNC = 'sendpicture'
PIC3D_FUNC = "sendply"
HTTP_TIMEOUT = 10

def send_file(url, params, file_path):
    path = file_path
    if platform=="win32":
        path=str(file_path)
    else:
        path=str(file_path)
    try:
        #req = requests.post(url, timeout=HTTP_TIMEOUT, files={"picture": path}, data=params)
        filename = os.path.basename(file_path)
        req = requests.post(url, timeout=HTTP_TIMEOUT, files={"picture": (filename, open(path,'rb'))}, data=params)
        #req = requests.post(url, timeout=HTTP_TIMEOUT, files={"picture":  path}, data=params)
    except requests.exceptions.RequestException as ex:
        print(ex)
        return False
    if req.status_code == requests.codes.ok:  #pylint: disable=no-member
        return True
    else:
        print('Noget gik galt: ', req.status_code)
        print(req.text)
    return False

def send_ply_picture(deviceid, file_path):
    url = API_SERVER + PIC3D_FUNC
    param = {'deviceid': deviceid, 'mypicture': file_path}
    result = send_file(url, param, file_path)
    return result

def send_picture(deviceid, file_path):
    url = API_SERVER + PIC2D_FUNC
    param = {'deviceid': deviceid, 'mypicture': file_path}
    result = send_file(url, param, file_path)
    return result
