"""
api views
"""
import os
import time
import logging
#from pathlib import Path
from shutil import copy
#from threading import Thread
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse #, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from compute.settings import DEVICE_PATH, SCAN_3D_PICTURE #, NN_ENABLE #, TEMP_PATH
from api.utils import filename_number, start_scan,  stop_scan #, test_nn
from calibrate.functions import cal_camera
from scan3d.receivescan import receive_scan # process_scan,

# pylint:disable=logging-fstring-interpolation

_DEBUG = True
_TIMING = True
_PROCESS_BACKGROUND = True

log = logging.getLogger(__name__)

def index(request):
    "api index"
    return render(request, 'api_index.html')

def save_uploaded_file(handle, filepath):
    "save a filehandle in filepath"
    with open(filepath, 'wb+') as destination:
        for chunk in handle.chunks():
            destination.write(chunk)

def device_folder(request):
    "Find folder part for device"
    deviceid = request.POST.get('deviceid', "nodevice")
    device_path = DEVICE_PATH / deviceid
    os.makedirs(device_path, exist_ok=True)
    return device_path

# def get_device_folder(deviceid):
#     device_path = DEVICE_PATH / deviceid
#     os.makedirs(device_path, exist_ok=True)
#     return device_path

def check_device(request):
    "get deviceid"
    #TODO check if ok
    deviceid = request.POST.get('deviceid', request.GET.get('deviceid'))
    return deviceid

def start(request):
    "Common start function"
    if not request.method in ['GET','POST']:
        return JsonResponse({'result':"False", "reason": "illegal method"},status=400)
    deviceid = check_device(request)
    if not deviceid:
        return HttpResponse('start2d must include deviceid', status=400)
    devicefolder = device_folder(request)
    start_scan(deviceid, devicefolder)
    return JsonResponse({'result':"OK"})

# ***************** 2D *******************
@csrf_exempt
def start2d(request):
    "Start 2D scan"
    cmd = request.POST.get('cmd', None)
    print("POST cmd:", cmd)
    cmd = request.GET.get('cmd', None)
    print("GET cmd:", cmd)
    return start(request)

@csrf_exempt
def save2d(request):
    "Save a 2d scan picture"
    if not request.method in ['POST']:
        return JsonResponse({'result':"False", "reason": "illegal method"})
    deviceid = check_device(request)
    devicefolder = device_folder(request)
    if not deviceid:
        return HttpResponse('save2d must include deviceid',sttus=400)
    datafolder = devicefolder / 'input'
    os.makedirs(datafolder, exist_ok=True)
    set_number = request.POST['pictureno']
    for i in request.FILES:
        flist = request.FILES.getlist(i)
        for j in flist:
            newname = filename_number(j.name, int(set_number))
            filepath = datafolder / newname
            save_uploaded_file(j, filepath)
    return JsonResponse({'result':"OK"})

@csrf_exempt
def stop2d(request):
    "Stop 2d scan"
    if not request.method in ['GET','POST']:
        return JsonResponse({'result':"False", "reason": "illegal method"}, status=400)
    deviceid = check_device(request)
    if not deviceid:
        return HttpResponse('stop2d must include deviceid',status=400)
    devicefolder = device_folder(deviceid)
    if _DEBUG:
        print("stop2d received: ", devicefolder)
    return JsonResponse({'result':"OK"})

# *************** 3D *********************
@csrf_exempt
def start3d(request):
    "start 3d scan - prepare for files"
    time_start = time.perf_counter()
    # remove last results
    res = start(request)
    time_stop = time.perf_counter()
    if _TIMING:
        log.info(f"Start Scan API done in {time_stop - time_start:.3f} seconds")
    return res

@csrf_exempt
def scan3d(request):
    "receive 3d scan set"
    if request.method in ['POST']:
        time_start = time.perf_counter()
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
        if SCAN_3D_PICTURE == 1:
            # copy fringe picture to last_picture to show in UI
            copy(folder / 'dias.jpg', devicefolder / 'input' / 'last_picture.jpg')
        if _PROCESS_BACKGROUND:
            pass
        else:
            receive_scan(deviceid, folder)
        time_end = time.perf_counter()
        if _TIMING:
            log.info(f"Scan3d API done in {time_end - time_start:.3f} seconds")
        return JsonResponse({'result':"OK"})
    return JsonResponse({'result':"False", "errortext":"request is not post"}, status=400)

@csrf_exempt
def stop3d(request):
    "cleanup after 3d scan"
    if request.method in ['GET','POST']:
        deviceid = check_device(request)
        devicefolder = device_folder(request)
        stop_scan(deviceid, devicefolder)
        return JsonResponse({'result':"OK"})
    return JsonResponse({'result':"False", "reason": "Missing deviceid"}, status=400)

############### Sendfiles ##################

def save_files_to_folder(request, datafolder):
    "save a file to dedicated folder"
    os.makedirs(datafolder, exist_ok=True)
    for i in request.FILES:
        flist = request.FILES.getlist(i)
        for j in flist:
            filepath = datafolder / j.name
            save_uploaded_file(j, filepath)

@csrf_exempt
def sendfiles(request):
    "send special file request"
    if request.method in ['POST']:
        deviceid = check_device(request)
        devicefolder = device_folder(request)
        cmd = request.POST.get('cmd', None)
        if cmd=="calcamera":
            datafolder = devicefolder / 'calibrate' / 'camera'
            save_files_to_folder(request, datafolder)
            cal_camera(deviceid, datafolder)
            return JsonResponse({'result':"OK"})
        if cmd == "calflash":
            print("Calibrate flash led")
            datafolder = devicefolder / 'calibrate' / 'calcamera'
            return JsonResponse({'result':"OK"})
        print("unknown cmd: ", cmd)
        datafolder = devicefolder / 'unknown_cmd'
        save_files_to_folder(request, datafolder)
        return JsonResponse({'result':"OK"})
    return JsonResponse({'result':"False", "reason": "Missing deviceid"},status=400)
