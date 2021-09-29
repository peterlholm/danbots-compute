"""
api views
"""
import os
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from compute.settings import DATA_PATH #, NN_ENABLE #, TEMP_PATH
from api.utils import receive_pictures
from api.device_config import read_config, save_config
#from compute3d.receive import start_scan,  stop_scan, test_nn # receive_pic_set,
from api.utils import start_scan,  stop_scan #, test_nn # receive_pic_set,
from nn.receive import receive_pic_set
from Utils.Imaging.calibrering.calibrate import get_img_slope, get_img_freq
from .forms import Form3dScan

DEVICE_PATH = DATA_PATH / 'device'

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

# 2D
@csrf_exempt
def start2d(request):
    if not request.method in ['GET','POST']:
        return JsonResponse({'result':"False", "reason": "illegal method"})
    deviceid = check_device(request)
    if not deviceid:
        return HttpResponse('start2d must include deviceid')
    devicefolder = get_device_folder(deviceid)
    print("start2d received: ", devicefolder)
    return JsonResponse({'result':"OK"})

@csrf_exempt
def save2d(request):
    if not request.method in ['POST']:
        return JsonResponse({'result':"False", "reason": "illegal method"})
    deviceid = check_device(request)
    if not deviceid:
        return HttpResponse('save2d must include deviceid')
    #devicefolder = get_device_folder(deviceid)
    file = request.FILES['picture']
    print(file)
    print(file.content_type)
    print("save2d received: ")
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

# 3D
@csrf_exempt
def start3d(request):
    if request.method =="GET":
        if request.GET.get('deviceid') is None:
            return HttpResponse('start3d must include deviceid')
    if request.method in ['GET','POST']:
        devicefolder = device_folder(request)
        start_scan(devicefolder)
        return JsonResponse({'result':"OK"})
    return JsonResponse({'result':"False", "reason": "illegal method"})

@csrf_exempt
def save3d(request):
    picform = Form3dScan(initial={'deviceid': 123})
    if request.method == 'POST':
        picform = Form3dScan(request.POST, request.FILES)
        if picform.is_valid():
            devicefolder = device_folder(request)
            set_number = request.POST['pictureno']
            receive_pictures(devicefolder, set_number, request.FILES['color_picture'], request.FILES['dias_picture'],request.FILES['noLight_picture'])
            return JsonResponse({'result':"OK"})
        print ("Form not valid", picform.errors)
    mycontext = {
        'form': picform,
    }
    #print(mycontext)
    return render(request, 'send3dscan.html', mycontext)

@csrf_exempt
def scan3d(request):
    picform = Form3dScan(initial={'deviceid': 123})
    mycontext = {
        'form': picform,
    }
    if request.method == 'POST':
        picform = Form3dScan(request.POST, request.FILES)
        if picform.is_valid():
            devicefolder = device_folder(request)
            set_number = request.POST['pictureno']
            receive_pic_set(devicefolder, set_number, request.FILES['color_picture'], request.FILES['dias_picture'],request.FILES['noLight_picture'])
            return JsonResponse({'result':"OK"})
        print ("Form not valid", picform.errors)
    return render(request, 'send3dscan.html', mycontext)

@csrf_exempt
def stop3d(request):
    if request.method in ['GET','POST']:
        devicefolder = device_folder(request)
        stop_scan(devicefolder)
        return JsonResponse({'result':"OK"})
    return JsonResponse({'result':"False", "reason": "Missing deviceid"})

# sendfiles

@csrf_exempt
def sendfiles(request):
    if request.method in ['POST']:
        devicefolder = device_folder(request)
        cmd = request.POST['cmd']
        if cmd == "calibrate":
            print("Calibrate")
            datafolder = devicefolder / 'calibrate'
            os.makedirs(datafolder, exist_ok=True)
            for i in request.FILES:
                flist = request.FILES.getlist(i)
                for j in flist:
                    filepath = datafolder / j.name
                    save_uploaded_file(j, filepath)
            cal_picture = datafolder / 'color.png'
            slope = get_img_slope(cal_picture)
            freq = get_img_freq(cal_picture)
            print(slope,freq)
            config = read_config(devicefolder)
            config['calibrate'] = {'calibrate': True, "slope": slope, "frequency": freq }
            save_config(config, devicefolder )
            return JsonResponse({'result':"OK", "slope": slope, "frequency": freq})
        if cmd == "calflash":
            print("Calibrate flash")
            datafolder = devicefolder / 'calibrate' / 'calflash'
            os.makedirs(datafolder, exist_ok=True)
            for i in request.FILES:
                print(i)
                flist = request.FILES.getlist(i)
                for j in flist:
                    print(j)
                    filepath = datafolder / j.name
                    save_uploaded_file(j, filepath)
            return JsonResponse({'result':"OK"})
        print("unknown cmd: ", cmd)
        return HttpResponse("Unknown command")
        #return JsonResponse({'result':"OK", "slope": 0})
    return JsonResponse({'result':"False", "reason": "Missing deviceid"})
