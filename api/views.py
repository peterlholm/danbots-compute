import os
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from compute.settings import DATA_PATH #, NN_ENABLE #, TEMP_PATH
from api.utils import receive_pictures
from compute3d.receive import start_scan, receive_pic_set, stop_scan, test_nn
from .forms import Form3dScan

DEVICE_PATH = DATA_PATH / 'device'

def save_uploaded_file(handle, filepath):
    with open(filepath, 'wb+') as destination:
        for chunk in handle.chunks():
            destination.write(chunk)

def device_folder(request):
    deviceid = request.POST.get('deviceid', "1234")
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
    devicefolder = get_device_folder(deviceid)
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

@csrf_exempt
def test3d(request):
    print("test3d request - calling test_nn")
    result = test_nn()
    return JsonResponse({ **result, 'result':"OK"})
