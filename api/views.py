#import os
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
#from compute.settings import DATA_PATH

from compute3d.receive import start_scan, receive_pic_set, stop_scan, test_nn

from .forms import Form3dScan
#from .scan3d import receive_pic_set, stop_scan

def save_uploaded_file(handle, filepath):
    with open(filepath, 'wb+') as destination:
        for chunk in handle.chunks():
            destination.write(chunk)

@csrf_exempt
def start3d(request):
    if request.method == 'POST':
        deviceid = request.POST['deviceid']
        start_scan(deviceid)
        return JsonResponse({'result':"OK"})
    if request.method == 'GET':
        deviceid = request.GET['deviceid']
        start_scan(deviceid)
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
            deviceid = request.POST['deviceid']
            set_number = request.POST['pictureno']
            #data_folder = DATA_PATH
            #os.makedirs(data_folder, exist_ok=True)
            receive_pic_set(deviceid, set_number, request.FILES['color_picture'], request.FILES['french_picture'],request.FILES['noLight_picture'])
            return JsonResponse({'result':"OK"})
        print ("Form not valid", picform.errors)
    return render(request, 'send3dscan.html', mycontext)

@csrf_exempt
def stop3d(request):
    if request.method == 'POST':
        deviceid = request.POST['deviceid']
        stop_scan(deviceid)
        return JsonResponse({'result':"OK"})
    return JsonResponse({'result':"False", "reason": "Missing deviceid"})
