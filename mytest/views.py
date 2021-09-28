"""
mytest views.py
test funtion til servere
"""

import subprocess
from os import name
from pathlib import Path
from django.http import FileResponse
from django.shortcuts import render, HttpResponse, redirect
#from send2live.send2live import send_file
from send2live.send2live import send_picture, send_ply_picture
from mytest.send2device import send_start_scan

from compute.settings import DATA_PATH, MYDEVICE #, API_SERVER, TEMP_PATH
from calibrate.flash import flash_led_test

def index(request):
    return render (request, 'index.html')

def start_scan(request):
    device_path = "/data/device/" + MYDEVICE + "/input/1/"
    res = send_start_scan()
    if res:
        return redirect("/nn/showresult?folder="+device_path)
    return HttpResponse("Scan start gik galt", res)

def home(request):
    return render (request, 'home.html')

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
    flash_led_test()
    return HttpResponse("OK")
