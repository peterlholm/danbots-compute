"""
api views
"""
import os
#from time import sleep
#from threading import Thread
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse #, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from compute.settings import DEVICE_PATH #, NN_ENABLE #, TEMP_PATH
#from api.utils import receive_pictures
from api.utils import filename_number, start_scan,  stop_scan #, test_nn # receive_pic_set,
from calibrate.functions import cal_camera
from scan3d.receivescan import receive_scan
#from .forms import Form3dScan
#from api.device_config import read_config, save_config
#from compute3d.receive import start_scan,  stop_scan, test_nn # receive_pic_set,
#from nn.receive import receive_pic_set
#from Utils.Imaging.calibrering.calibrate import get_img_slope, get_img_freq
#from calibrate.mask import create_mask, save_flash_mask, save_dias_mask

_DEBUG = True

def index(request):
    return render(request, 'api_index.html')

def save_uploaded_file(handle, filepath):
    with open(filepath, 'wb+') as destination:
        for chunk in handle.chunks():
            destination.write(chunk)

def device_folder(request):
    deviceid = request.POST.get('deviceid', "nodevice")
    device_path = DEVICE_PATH / deviceid
    os.makedirs(device_path, exist_ok=True)
    return device_path

def get_device_folder(deviceid):
    device_path = DEVICE_PATH / deviceid
    os.makedirs(device_path, exist_ok=True)
    return device_path

def check_device(request):
    deviceid = request.POST.get('deviceid', request.GET.get('deviceid'))
    return deviceid

def start(request):
    if not request.method in ['GET','POST']:
        return JsonResponse({'result':"False", "reason": "illegal method"})
    deviceid = check_device(request)
    if not deviceid:
        return HttpResponse('start2d must include deviceid')
    devicefolder = device_folder(request)
    start_scan(deviceid, devicefolder)
    return JsonResponse({'result':"OK"})

# ***************** 2D *******************
@csrf_exempt
def start2d(request):
    return start(request)

@csrf_exempt
def save2d(request):
    if not request.method in ['POST']:
        return JsonResponse({'result':"False", "reason": "illegal method"})
    deviceid = check_device(request)
    devicefolder = device_folder(request)
    if not deviceid:
        return HttpResponse('save2d must include deviceid')
    datafolder = devicefolder / 'input'
    os.makedirs(datafolder, exist_ok=True)
    set_number = request.POST['pictureno']
    #print ("set", set_number)
    for i in request.FILES:
        flist = request.FILES.getlist(i)
        for j in flist:
            #print(j)
            newname = filename_number(j.name, int(set_number))
            filepath = datafolder / newname
            save_uploaded_file(j, filepath)
    return JsonResponse({'result':"OK"})

@csrf_exempt
def stop2d(request):
    if not request.method in ['GET','POST']:
        return JsonResponse({'result':"False", "reason": "illegal method"})
    deviceid = check_device(request)
    if not deviceid:
        return HttpResponse('stop2d must include deviceid')
    devicefolder = get_device_folder(deviceid)
    print("stop2d received: ", devicefolder)
    return JsonResponse({'result':"OK"})

# *************** 3D *********************
@csrf_exempt
def start3d(request):
    return start(request)
    # if request.method =="GET":
    #     if request.GET.get('deviceid') is None:
    #         return HttpResponse('start3d must include deviceid')
    # if request.method in ['GET','POST']:
    #     deviceid = check_device(request)
    #     devicefolder = device_folder(request)
    #     start_scan(deviceid, devicefolder)
    #     return JsonResponse({'result':"OK"})
    # return JsonResponse({'result':"False", "reason": "illegal method"})

@csrf_exempt
def scan3d(request):
    if request.method in ['POST']:
        #cmd = request.POST.get('cmd', None)
        deviceid = check_device(request)
        devicefolder = device_folder(request)
        set_number = request.POST['pictureno']
        folder = devicefolder / 'input' / str(set_number)
        os.makedirs(folder, exist_ok=True)
        for i in request.FILES:
            flist = request.FILES.getlist(i)
            for j in flist:
                filepath = folder / j.name
                save_uploaded_file(j, filepath)
                # if j.name=="dias.jpg":
                #     save_uploaded_file(j, devicefolder / 'input' / 'last_dias.jpg')
        receive_scan(deviceid, folder)
        return JsonResponse({'result':"OK"})
    return JsonResponse({'result':"False", "errortext":"request is not post"})

@csrf_exempt
def stop3d(request):
    if request.method in ['GET','POST']:
        deviceid = check_device(request)
        devicefolder = device_folder(request)
        stop_scan(deviceid, devicefolder)
        return JsonResponse({'result':"OK"})
    return JsonResponse({'result':"False", "reason": "Missing deviceid"})

##################################################################

def save_file_to_folder(request, datafolder):
    os.makedirs(datafolder, exist_ok=True)
    for i in request.FILES:
        flist = request.FILES.getlist(i)
        for j in flist:
            filepath = datafolder / j.name
            save_uploaded_file(j, filepath)

@csrf_exempt
def sendfiles(request):
    if request.method in ['POST']:
        deviceid = check_device(request)
        devicefolder = device_folder(request)
        cmd = request.POST.get('cmd', None)
        if cmd=="calcamera":
            datafolder = devicefolder / 'calibrate' / 'camera'
            save_file_to_folder(request, datafolder)
            cal_camera(deviceid, datafolder)
            return JsonResponse({'result':"OK"})
        # if cmd == "caldias":
        #     print("Calibrate dias")
        #     datafolder = devicefolder / 'calibrate' / 'calcamera'
        #     save_file_to_folder(request, datafolder)
        #     cal_picture = datafolder / 'color.png'
        #     slope = get_img_slope(cal_picture)
        #     freq = get_img_freq(cal_picture)
        #     if _DEBUG:
        #         print(f"Callibrate device {deviceid} Slope: {slope}, Freq: {freq}")
        #     config = read_config(devicefolder)
        #     config['calibrate'] = {'calibrate': True, "slope": slope, "frequency": freq }
        #     save_config(config, devicefolder)
        #     create_masks(deviceid, datafolder)
        #     return JsonResponse({'result':"OK", "slope": slope, "frequency": freq})
        if cmd == "calflash":
            print("Calibrate flash led")
            datafolder = devicefolder / 'calibrate' / 'calcamera'
            return JsonResponse({'result':"OK"})

        print("unknown cmd: ", cmd)
        datafolder = devicefolder / 'unknown_cmd'
        save_file_to_folder(request, datafolder)
        return JsonResponse({'result':"OK"})
    return JsonResponse({'result':"False", "reason": "Missing deviceid"})
