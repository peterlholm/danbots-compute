"""
mytest views.py
test funtion til servere
"""

import subprocess
from os import name
from pathlib import Path
from time import sleep
from django.http import FileResponse, StreamingHttpResponse
from django.shortcuts import render, HttpResponse, redirect
from send2live.send2live import send_picture, send_ply_picture
from mytest.send2device import send_start_scan
from compute.settings import BASE_DIR, DATA_PATH, MYDEVICE #, API_SERVER, TEMP_PATH
from calibrate.flash import flash_led_test
from api.pic_utils import include_all_masks

def index(request):
    return render (request, 'index.html', context={ 'device': MYDEVICE })

def debug(request):
    return render (request, 'debug.html')

def start_scan(request):
    device_path = "/data/device/" + MYDEVICE + "/input/1/"
    res = send_start_scan()
    if res:
        return redirect("/nn/showresult?folder="+device_path)
    return HttpResponse("Scan start gik galt", res)


def install_models(request):
    return render (request, 'install_models.html')

def test(request):
    return HttpResponse("Hello, Django!")

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

def include_masks(request):
    folder = "data/device/b827eb05abc2/input"
    include_all_masks(Path(folder))
    return HttpResponse("OK")

# MJpeg streaming

def mjpeg_stream(file, file_watcher):
    #image_data = open(file, mode='rb').read()
    #first = True
    #boundary = b'--frame\r\n'
    #watcher = fFileWatcher(".")

    while True:
        #chunkheader = b"Content-Type: image/jpeg\nContent-Length: " + str(len(image_data)).encode('ascii') + b"\n\n"
        #boundary = b"\n--myboundary\n"
        #yield (chunkheader + image_data + boundary)
        # data = b''
        # if first:
        #     data += boundary
        #     first= False
        image_data = open(file, mode='rb').read()
        try:
            print ("Display...")
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + image_data + b'\r\n')
            # display twice for chrome
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + image_data + b'\r\n')
            #yield (b'Content-Type: image/jpeg\r\n\r\n' + image_data + b'\r\n' + boundary)
            sleep(1)
            #file_watcher.release()
        except Exception as ex:
            print("vi rydder op")
            print (ex)
            #file_watcher.close()
        #file_watcher.acquire()
    print ("slutter")

def pic_stream(request):
    #context = init_session_context(request)
    # clinic_no = request.session['clinic_no']
    # clinic_path = Path(request.session['clinic_path'])
    #filefolder = clinic_path / "2d/test.jpg"
    filefolder = BASE_DIR / "testdata/device/color.jpg"
    #print(clinic_no)
    print(filefolder)
    #sem = FileWatcher(".")
    sem = None
    #image_data = open(filefolder, mode='rb').read()
    #return HttpResponse(image_data, content_type="image/jpeg")
    stream = mjpeg_stream(filefolder, sem)
    return StreamingHttpResponse(stream, content_type='multipart/x-mixed-replace;boundary=frame')
