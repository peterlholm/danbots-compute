"""request from browsers"""
from pathlib import Path
from datetime import datetime
from time import sleep
from django.shortcuts import  HttpResponse #render,
from django.http import  StreamingHttpResponse #JsonResponse,
from django.views.decorators.csrf import csrf_exempt
#from tensorflow.python.client import device_lib
from compute.settings import BASE_DIR, DEVICE_PATH


#print (device_lib.list_local_devices())

def check_device(request):
    deviceid = request.POST.get('deviceid', request.GET.get('deviceid'))
    return deviceid

def get_device_folder(deviceid):
    device_path = DEVICE_PATH / deviceid
    if Path.exists(device_path):
        return device_path
    return None

# MJpeg streaming

NOFILE = BASE_DIR / 'web/static/web' / 'afventer.jpg'
SLEEP_TIME = 3

def mjpeg_stream(file):
    running = True
    with open(NOFILE, mode='rb') as fd:
        no_data = fd.read()
    while running:
        image_data = None
        try:
            with open(file, mode='rb') as fd:
                image_data = fd.read()
        except IOError: # as ex:
            #print("nodata", ex)
            image_data = no_data
        try:
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + image_data + b'\r\n')
        except Exception as ex:
            print("yield error")
            print (ex)
            running = False
        sleep(SLEEP_TIME)
    print ("slutter")

@csrf_exempt
def pic_stream(request):
    start_delay = 5
    print ("picstart picstream", datetime.now())
    deviceid = check_device(request)
    if not deviceid:
        print('pic_stream must include deviceid')
        return HttpResponse('pic_stream must include deviceid')
    devicefolder = get_device_folder(deviceid)
    sleep(start_delay)
    print ("picstart picstream sleep", datetime.now())
    file = devicefolder / 'input' / 'last_picture.jpg'
    stream = mjpeg_stream(file)
    return StreamingHttpResponse(stream, content_type='multipart/x-mixed-replace;boundary=frame')

@csrf_exempt
def pic(request):
    deviceid = check_device(request)
    if not deviceid:
        return HttpResponse('pic_stream must include deviceid')
    file = BASE_DIR / "testdata/device/color.jpg"
    with open(file, "rb") as fd:
        return HttpResponse(fd.read(), content_type="image/jpeg")
    return HttpResponse("noget gik galt")
