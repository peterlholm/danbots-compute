"""
# this module send results to API/Live server
"""
#from sys import platform
#import os.path
import requests
#from compute.settings import API_SERVER #, DATA_PATH,TEMP_PATH

PIC2D_FUNC = 'sendpicture'
PIC3D_FUNC = "sendply"
HTTP_TIMEOUT = 30

def send_request(url, params=None):
    try:
        req = requests.get(url, timeout=HTTP_TIMEOUT, data=params)
    except requests.exceptions.RequestException as ex:
        print(ex)
        return False
    if req.status_code == requests.codes.ok:  #pylint: disable=no-member
        return True
    print('Noget gik galt: ', req.status_code)
    print(req.text)
    return False

def send_start_scan(deviceurl="http://danwand.local:8080/"):
    cmd = "3d/3d"
    url = deviceurl + cmd
    print (url)
    res = send_request(url)
    print(res)
    return res
