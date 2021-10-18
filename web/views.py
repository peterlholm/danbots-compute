"""request from browsers"""
from pathlib import Path
from time import sleep
from django.shortcuts import  HttpResponse #render,
from django.http import  StreamingHttpResponse #JsonResponse,
from django.views.decorators.csrf import csrf_exempt
from compute.settings import BASE_DIR, DEVICE_PATH

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

def mjpeg_stream(file):
    running = True
    with open(NOFILE, mode='rb') as fd:
        no_data = fd.read()
    while running:
        image_data = None
        try:
            with open(file, mode='rb') as fd:
                image_data = fd.read()
        except IOError:
            image_data = no_data
        try:
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + image_data + b'\r\n')
        except Exception as ex:
            print("yield error")
            print (ex)
            running = False
        sleep(1)
    print ("slutter")

@csrf_exempt
def pic_stream(request):
    deviceid = check_device(request)
    if not deviceid:
        return HttpResponse('pic_stream must include deviceid')
    devicefolder = get_device_folder(deviceid)
    file = devicefolder / 'input' / 'last_dias.jpg'
    sleep(1)
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
