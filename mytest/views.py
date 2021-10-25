"""
mytest views.py
test funtion til servere
"""

import subprocess
from os import name
from shutil import rmtree
from pathlib import Path
#from time import sleep
from django.http import FileResponse #, StreamingHttpResponse
from django.shortcuts import render, HttpResponse, redirect
from send2live.send2live import send_picture, send_ply_picture
from mytest.send2device import send_start_scan
from compute.settings import BASE_DIR, DATA_PATH, DEVICE_PATH, MYDEVICE #, API_SERVER, TEMP_PATH
from calibrate.flash import flash_led_test
from calibrate.functions import cal_camera
from api.pic_utils import include_all_masks
from scan3d.receiveblender import receive_scan_set, prepare_blender_input

def index(request):
    return render (request, 'index.html', context={ 'device': MYDEVICE })

def debug(request):
    return render (request, 'debug.html')

def calibrate_camera(request):
    deviceid = MYDEVICE
    folder = DATA_PATH / 'device' / deviceid / 'calibrate/calcamera'
    cal_camera(deviceid, Path(folder))
    return HttpResponse("Calibration finish")

def show_pictures(request):
    """
    Show all jpg and png pictures in folder
    """
    datapath = 'testdata/process/'
    #datapath = 'testdata/'
    data_path = request.GET.get('folder', datapath)
    abs_path = DATA_PATH / data_path
    pic_list = []
    #print ("abs", abs_path)
    for pic in Path.glob(abs_path,"*.jpg"):
        pic_list.append("/data/"+data_path+pic.name)
    for pic in Path.glob(abs_path,"*.png"):
        pic_list.append("/data/"+data_path+pic.name)
    mycontext={"path": abs_path, "pictures": pic_list}
    #print (mycontext)
    return render (request, 'showresult.html', context=mycontext)

####### receive blender
TESTDATAFOLDER = BASE_DIR / "testdata" / "okt25" / "render5"

def receive_blender(request):
    data_path = DEVICE_PATH / 'blender' / 'input'
    print(data_path)
    if Path.exists(data_path):
        rmtree(data_path, ignore_errors=True)
    Path.mkdir(data_path, parents=True)
    infolder = Path(TESTDATAFOLDER)
    prepare_blender_input(infolder, data_path)
    receive_scan_set(data_path)
    return redirect("/test/show_pictures?folder=device/blender/input/")

####################################################
def start_scan(request):
    "Request scan from device and display results"
    device_path = "device/" + MYDEVICE + "/input/1/"
    res = send_start_scan()
    if res:
        return redirect("/test/show_pictures?folder="+device_path)
    return HttpResponse("Scan start gik galt", res)


def install_models(request):
    return render (request, 'install_models.html')

def test(request):
    return HttpResponse("Hello, Django!")

def sendply(request):
    path = DATA_PATH / "temp/faar.jpg"
    result = send_ply_picture("123", path)
    return HttpResponse("send_ply_picture: " + str(result))

def sendpicture(request):
    path = DATA_PATH / "temp/faar.jpg"
    result = send_picture("123", path)
    return HttpResponse("send_picture: " + str(result))

def errorlog(request):
    return FileResponse(open('/var/log/apache2/danbots/compute.err.log','rb'))

def upgrade(request):
    if name == 'nt':
        return HttpResponse("Not allowd")
    root = Path(__file__).resolve().parent.parent
    script = root / 'setup' / 'git_update.sh'
    print(script)
    result = subprocess.run(script, cwd=root, check=True)
    output = str(result)
    return HttpResponse(output)

def flash_led(request):
    device = "b827eb05abc2"
    flash_led_test(device)
    return HttpResponse("OK")

def include_masks(request):
    folder = "data/device/b827eb05abc2/input"
    include_all_masks(Path(folder))
    return HttpResponse("OK")
