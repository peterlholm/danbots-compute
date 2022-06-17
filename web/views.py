"""request from browsers"""
from pathlib import Path
#from datetime import datetime
from time import sleep
from django.shortcuts import  HttpResponse, render
from django.http import  StreamingHttpResponse #JsonResponse,
from django.views.decorators.csrf import csrf_exempt
from compute.settings import BASE_DIR, DEVICE_PATH #, NN_ENABLE
from calibrate.camera.calibration import calibrate_camera, save_device_camera_matrix
from calibrate.camera.distance import calc_dist

def check_device(request):
    "get the device id"
    # todo check is valid
    deviceid = request.POST.get('deviceid', request.GET.get('deviceid'))
    return deviceid

def get_device_folder(deviceid):
    "get the folder for the device"
    device_path = DEVICE_PATH / deviceid
    if Path.exists(device_path):
        return device_path
    return None

# MJpeg streaming

NOFILE = BASE_DIR / 'web/static/web' / 'afventer.jpg'
SLEEP_TIME = 3

def index(request):
    "index for prod web site"
    return render (request, 'web/index.html')

def calibratecamera(request):
    "calibrate camera based on folder with pictures"
    #cv2
    #chessboard = (9,6) ok
    #folder = BASE_DIR / 'calibrate/camera/testimages/cv2test/'
    #pizero
    # chessboard = (7,9)
    # folder = BASE_DIR / 'calibrate/camera/testimages/pizero/serie1/'
    # folder = BASE_DIR / 'calibrate/camera/testimages/pizero/serie2/'
    #danwand
    chessboard = (7,7)
    folder = BASE_DIR / 'calibrate/camera/testimages/danwand/serie1/'

    #folder = BASE_DIR / 'data/device/e45f013a21c7/input/'
    #folder = BASE_DIR / 'data/device/e45f013a21c7/input/'

    mtx, dist = calibrate_camera(folder, chessboard)
    print("calibration result", mtx, "dist", dist)
    save_device_camera_matrix("123", mtx, dist)
    return HttpResponse("Camera callibrated "+ str(mtx))

def distance(request):
    "get distance from picture with square"
    fimagefile = BASE_DIR / 'calibrate/camera/testimages/distance/picture6a.jpeg'
    imagefile = request.GET.get('image',fimagefile)
    dist = calc_dist(imagefile)
    print("Distance (mm):", dist)
    return HttpResponse("Distance to picture(mm): " + dist)

def mjpeg_stream(file):
    "stream the file to the browser"
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
    "get the standard picture stream for device"
    start_delay = 5
    #print ("picstart picstream", datetime.now())
    sleep(start_delay)
    deviceid = check_device(request)
    #print(deviceid)
    if not deviceid:
        print('pic_stream must include deviceid')
        return HttpResponse('pic_stream must include deviceid')
    devicefolder = get_device_folder(deviceid)
    #print ("picstart picstream sleep", datetime.now(), devicefolder)
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
