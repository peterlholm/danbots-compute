"""
mytest views.py
test funtion til servere
"""

#from datetime import datetime
import subprocess
from os import name
from shutil import rmtree, copy2
from pathlib import Path
from time import sleep
from django.http import FileResponse #, StreamingHttpResponse
from django.shortcuts import render, HttpResponse, redirect
from send2live.send2live import send_picture, send_ply_picture
from mytest.send2device import send_start_scan
from compute.settings import BASE_DIR, DATA_PATH, DEVICE_PATH, MYDEVICE, NN_ENABLE #, API_SERVER, TEMP_PATH
from calibrate.flash import flash_led_test
from calibrate.functions import cal_camera
#from api.pic_utils import include_all_masks
from scan3d.receiveblender import receive_blender_set #prepare_blender_input
from scan3d.receivescan import receive_scan, process_scan
from scan3d.processing import copy_test_set, copy_jpg_test_set, copy_stitch_test_set # copy_blender_test_set
from stitching.stitch import stitch_run

def index(request):
    return render (request, 'index.html', context={ 'device': MYDEVICE })

def debug(request):
    return render (request, 'debug.html')

def calibrate_camera(request):
    deviceid = MYDEVICE
    folder = DATA_PATH / 'device' / deviceid / 'calibrate/calcamera'
    cal_camera(deviceid, Path(folder))
    return HttpResponse("Calibration finish")

############### show pictures #################
def show_pictures(request):
    """
    Show all jpg and png pictures in folder
    """
    datapath = 'testdata/process/'
    #datapath = 'testdata/'
    data_path = request.GET.get('folder', datapath)
    number = request.GET.get('number',None)
    if number:
        sdata_path = data_path + str(number) + '/'
    else:
        sdata_path = data_path
    abs_path = DATA_PATH / sdata_path
    #print(abs_path)
    pic_list = []
    #print ("abs", abs_path)
    for pic in Path.glob(abs_path,"*.jpg"):
        pic_list.append("/data/"+sdata_path+pic.name)
    for pic in Path.glob(abs_path,"*.png"):
        pic_list.append("/data/"+sdata_path+pic.name)
    nextfolder = ''
    prevfolder=''
    if number:
        nextfolder = data_path + '&number=' + str(int(number)+1)
        prevfolder = data_path + '&number=' + str(int(number)-1)
    link = "http:/test/show_pictures?folder=" + nextfolder
    linkprev = "http:/test/show_pictures?folder=" + prevfolder
    mycontext={"path": abs_path, "pictures": pic_list, "link": link, "linkprev": linkprev}
    #print (mycontext)
    return render (request, 'showresult.html', context=mycontext)

def show5(request):
    datapath = 'device/' + MYDEVICE +'/input/'
    data_path = request.GET.get('folder', datapath)
    number = request.GET.get('folder', 5) + 1
    abs_path = DATA_PATH / data_path
    pic_list = []
    for i in range(1,number):
        pic_list.append("/data/"+data_path+'/'+str(i)+'/dias.jpg')
    for i in range(1,number):
        pic_list.append("/data/"+data_path+'/'+str(i)+'/fringe.png')
    for i in range(1,number):
        pic_list.append("/data/"+data_path+'/'+str(i)+'/nnwrap1.png')
    for i in range(1,number):
        pic_list.append("/data/"+data_path+'/'+str(i)+'/pointcloud.jpg')
    mycontext={"path": abs_path, "pictures": pic_list, "link": "", "linkprev": ''}
    return render (request, 'showresult.html', context=mycontext)

def show5sequense(request, data_path, dias=True):
    #datapath = 'device/' + MYDEVICE +'/input/'
    #data_path = request.GET.get('folder', datapath)
    #number = request.GET.get('folder', 5) + 1
    number = 6
    abs_path = DATA_PATH / data_path
    pic_list = []
    for i in range(1,number):
        if dias:
            pic_list.append("/data/"+data_path+'/'+str(i)+'/dias.jpg')
    for i in range(1,number):
        pic_list.append("/data/"+data_path+'/'+str(i)+'/fringe.png')
    for i in range(1,number):
        pic_list.append("/data/"+data_path+'/'+str(i)+'/nnwrap1.png')
    for i in range(1,number):
        pic_list.append("/data/"+data_path+'/'+str(i)+'/pointcloud.jpg')
    mycontext={"path": abs_path, "pictures": pic_list, "link": "", "linkprev": ''}
    return render (request, 'showresult.html', context=mycontext)

def showblender5(request):
    datapath = 'device/blender/input/'
    return show5sequense(request, datapath, dias=False)

####### process scan #######
def proc_scan(request):
    data = DEVICE_PATH / MYDEVICE
    data_path = data / 'input/1/'
    #print(data_path)
    receive_scan(MYDEVICE, data_path)
    return redirect("/test/show_pictures?folder=device/" + MYDEVICE + "/input/1/")

####### receive folder

def rec_folder(request):
    data = DEVICE_PATH / 'folder'
    data_path = DEVICE_PATH / 'folder' / 'input'
    print(data_path)
    if Path.exists(data_path):
        rmtree(data_path, ignore_errors=True)
    Path.mkdir(data_path, parents=True)
    infolder = Path(data)
    copy2(infolder / 'color.png', data_path / 'color.png')
    copy2(infolder / 'fringe.png', data_path / 'fringe.png')
    copy2(infolder / 'nolight.png', data_path / 'nolight.png')
    #prepare_blender_input(infolder, data_path)
    receive_scan('folder', data_path)
    return redirect("/test/show_pictures?folder=device/folder/input/")

####### receive blender   ##################

TESTDATAFOLDER = BASE_DIR / "testdata" / "renders211105" / "render14"
#TESTDATAFOLDER = BASE_DIR / "testdata" / "renders211105" / "render23044"

def receive_blender(request):
    data_path = DEVICE_PATH / 'blender' / 'input' / '1'
    if Path.exists(data_path):
        rmtree(data_path, ignore_errors=True)
    Path.mkdir(data_path, parents=True)
    infolder = Path(TESTDATAFOLDER)
    #prepare_blender_input(infolder, data_path)
    receive_blender_set(infolder, data_path)
    return redirect("/test/show_pictures?folder=device/blender/input/1/")

def receive_blender5(request):
    folder_path = DEVICE_PATH / 'blender' / 'input'
    data_path = folder_path / '1'
    if Path.exists(data_path):
        rmtree(data_path, ignore_errors=True)
    Path.mkdir(data_path, parents=True)
    infolder = Path(TESTDATAFOLDER)
    #prepare_blender_input(infolder, data_path)
    receive_blender_set(infolder, data_path)
    copy_test_set(folder_path)
    for i in range(2,6):
        print( folder_path / str(i))
        #receive_scan(MYDEVICE, DEVICE_PATH / MYDEVICE / 'input' / str(i))
        process_scan('blender', folder_path / str(i))
    # wait for processing
    return redirect("/test/show_pictures?folder=device/blender/input/&number=1")
    #return redirect("/test/show_pictures?folder=device/blender/input/")

#################### SCAN ################################

def start_scan(request):
    "Request scan from device and display results"
    #print("Send start scan to device:" + MYDEVICE)
    device_path = "device/" + MYDEVICE + "/input/1/"
    res = send_start_scan()
    if res:
        # wait for processing
        sleep(0.5)
        if NN_ENABLE:
            sleep(8)
        return redirect("/test/show_pictures?folder="+device_path)
    return HttpResponse("Scan start gik galt", res)

def start_scan5(request):
    "Request scan from device and display results"
    res = send_start_scan()
    if res:
        sleep(11)
        copy_jpg_test_set(DEVICE_PATH / MYDEVICE / 'input')
        for i in range(2,6):
            receive_scan(MYDEVICE, DEVICE_PATH / MYDEVICE / 'input' / str(i))
            #process_scan(MYDEVICE, DEVICE_PATH / MYDEVICE / 'input' / str(i))
        return redirect("/test/show_pictures?folder=device/" + MYDEVICE + "/input/&number=1")
    return HttpResponse("Scan start gik galt", res)

def calc5(request):
    "Request scan from device and display results"
    print("Recalculate 4 pictures:" + MYDEVICE)
    copy_jpg_test_set(DEVICE_PATH / MYDEVICE / 'input')
    device_path = "device/" + MYDEVICE + "/input/1/"
    for i in range(1,6):
        print("Recalculating", DEVICE_PATH / MYDEVICE / 'input' / str(i))
        receive_scan(MYDEVICE, DEVICE_PATH / MYDEVICE / 'input' / str(i))
    return redirect("/test/show_pictures?folder=device/"+device_path)

################## STITCH ################
STITCH_SET = BASE_DIR / "testdata" / "renders211105"
def gen_stitch(request):
    "Stich 2 pcl"
    device = 'stitch'
    ofolder = DEVICE_PATH / device / 'stitch'
    print("Stitch: " + device)
    copy_stitch_test_set(STITCH_SET, ofolder )

    return redirect("/test/show_pictures?folder=device/"+device+"/stitch/&number=1")

def stitch_folder(request):
    device = 'stitch'
    folder = DEVICE_PATH / device / 'stitch'
    stitch_run(folder)
    return redirect("/test/show_pictures?folder=device/"+device+"/stitch/")


############# DOC ########################

def install_models(request):
    return render (request, 'install_models.html')

#############  send to live #################
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
