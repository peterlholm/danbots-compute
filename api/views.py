import os
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from compute.settings import DATA_PATH #, NN_ENABLE #, TEMP_PATH
from compute3d.receive import start_scan, receive_pic_set, stop_scan, test_nn
from .forms import Form3dScan

DEVICE_PATH = DATA_PATH / 'device'

def save_uploaded_file(handle, filepath):
    with open(filepath, 'wb+') as destination:
        for chunk in handle.chunks():
            destination.write(chunk)

def device_folder(request):
    deviceid = request.POST['deviceid']
    device_path = DEVICE_PATH / deviceid
    os.makedirs(device_path, exist_ok=True)
    return device_path

@csrf_exempt
def start3d(request):
    if request.method in ['GET','POST']:
        devicefolder = device_folder(request)
        start_scan(devicefolder)
        return JsonResponse({'result':"OK"})
    return JsonResponse({'result':"False", "reason": "Missing deviceid"})

@csrf_exempt
def test3d(request):
    print("test3d request - calling test_nn")
    result = test_nn()
    return JsonResponse({ **result, 'result':"OK"})

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
            receive_pic_set(devicefolder, set_number, request.FILES['color_picture'], request.FILES['french_picture'],request.FILES['noLight_picture'])
            return JsonResponse({'result':"OK"})
        print ("Form not valid", picform.errors)
    return render(request, 'send3dscan.html', mycontext)

@csrf_exempt
def stop3d(request):
    if request.method == 'POST':
        devicefolder = device_folder(request)
        stop_scan(devicefolder)
        return JsonResponse({'result':"OK"})
    return JsonResponse({'result':"False", "reason": "Missing deviceid"})
