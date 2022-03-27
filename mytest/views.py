"""
mytest views.py
test funtion til servere
"""
import subprocess
from os import name
from shutil import rmtree, copy2
from pathlib import Path
from time import sleep
from django.http import FileResponse, HttpResponseRedirect #, StreamingHttpResponse
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from send2live.send2live import send_picture, send_ply_picture
from mytest.send2device import send_start_scan
from compute.settings import BASE_DIR, DATA_PATH, DEVICE_PATH, MYDEVICE, NN_ENABLE #, API_SERVER, TEMP_PATH
from calibrate.flash import gen_flash_correction
from calibrate.functions import cal_camera
from scan3d.processing import process as process_3d
from scan3d.receiveblender import receive_blender_set, process_blender #prepare_blender_input
from scan3d.receivescan import receive_scan #, process_scan
from scan3d.test_set import copy_scan_set,copy_folder_set, copy_jpg_test_set, copy_test_set, copy_stitch_test_set #, rename_blender_files_set
from stitching.stitch import stitch_run, read_model_pcl
from stitching.meshing import mesh_run
from utils.img2img import img2img
from .convert_testset import convert2samir, zipfolder
from .forms import UploadScanSetFileForm, DeviceForm

def save_uploaded_file(handle, filepath):
    with open(filepath, 'wb+') as destination:
        for chunk in handle.chunks():
            destination.write(chunk)
# index

def index(request):
    return render (request, 'index.html', context={ 'device': MYDEVICE })

def test(request):
    return render (request, 'test.html', context={'blenderset': TESTDATAFOLDER })

def debug(request):
    return render (request, 'debug.html')

############### show pictures #################

def show_pictures(request):
    """
    Show all jpg and png pictures in folder
    """
    datapath = 'testdata/process/'
    data_path = request.GET.get('folder', datapath)
    if data_path[-1] != '/':
        data_path += '/'
    number = request.GET.get('number',None)
    if number:
        sdata_path = data_path + str(number) + '/'
    else:
        sdata_path = data_path
    abs_path = DATA_PATH / sdata_path
    pic_list = []
    for pic in Path.glob(abs_path,"*.jpg"):
        pic_list.append("/data/"+sdata_path+pic.name)
    for pic in Path.glob(abs_path,"*.png"):
        pic_list.append("/data/"+sdata_path+pic.name)
    link = linkprev = None
    if number:
        nextfolder = data_path + '&number=' + str(int(number)+1)
        prevfolder = data_path + '&number=' + str(int(number)-1)
        link = "http:/test/show_pictures?folder=" + nextfolder
        linkprev = "http:/test/show_pictures?folder=" + prevfolder
    mycontext={"path": abs_path, "pictures": pic_list, "link": link, "linkprev": linkprev}
    return render (request, 'show_pictures.html', context=mycontext)

def add_pic_list(pic_list, rel_data_path, file_name, maxnumber):
    # rel_data_path without /data
    r_path = "/data/" + rel_data_path
    a_path = DATA_PATH / rel_data_path
    for i in range(1,maxnumber):
        rpath =  r_path + str(i) + '/' + file_name
        apath = a_path / str(i) / file_name
        if apath.exists():
            pic_list.append(rpath)

def show_set(request):
    # show dedicate picture in folder set 1,2,3    
    data_path = request.GET.get('folder', 'device/folder/input/')
    if data_path[-1] != '/':
        data_path += '/'
    abs_path = DATA_PATH / data_path
    #rel_path = "/data/" + data_path
    pic_list = []
    number = int(request.GET.get('number', "100")) + 1
    maxnumber = 1
    while Path(abs_path / str(maxnumber)).exists():
        maxnumber += 1
    maxnumber = min(maxnumber, number)
    for i in range(1,maxnumber):
        pic_list.append("/data/"+data_path+str(i)+'/dias.jpg')
    # for i in range(1,maxnumber):
    #     pic_list.append("/data/"+data_path+str(i)+'/fringe.png')
    add_pic_list(pic_list, data_path, 'fringe.png', maxnumber)
    add_pic_list(pic_list, data_path, 'nnwrap1.png', maxnumber)
    add_pic_list(pic_list, data_path, 'pointcloud.jpg', maxnumber)
    mycontext={"path": abs_path, "pictures": pic_list, "link": "", "linkprev": ''}
    return render (request, 'show_pictures.html', context=mycontext)

def show_stitch_set(request):
    # show stitch debug picture in folder set 1,2,3    
    data_path = request.GET.get('folder', 'device/folder/input/')
    if data_path[-1] != '/':
        data_path += '/'
    abs_path = DATA_PATH / data_path
    #rel_path = "/data/" + data_path
    pic_list = []
    number = int(request.GET.get('number', "100")) + 1
    maxnumber = 1
    while Path(abs_path / str(maxnumber)).exists():
        maxnumber += 1
    maxnumber = min(maxnumber, number)
    for i in range(1,maxnumber):
        pic_list.append("/data/"+data_path+str(i)+'/dias.jpg')
    # for i in range(1,maxnumber):
    #     pic_list.append("/data/"+data_path+str(i)+'/fringe.png')
    #add_pic_list(pic_list, data_path, 'fringe.png', maxnumber)
    #(pic_list, data_path, 'nnwrap1.png', maxnumber)
    add_pic_list(pic_list, data_path, 'pointcloud.jpg', maxnumber)
    r_path = "/data/" + data_path
    #a_path = DATA_PATH / rel_data_path
    for i in range(1,maxnumber):
        rpath =  f"{r_path}in{i:02}.jpg"
        pic_list.append(rpath)
    for i in range(1,maxnumber):
        rpath2 =  f"{r_path}clean{i:02}.jpg"
        pic_list.append(rpath2)

    mycontext={"path": abs_path, "pictures": pic_list, "link": "", "linkprev": ''}
    return render (request, 'show_pictures.html', context=mycontext)

# device operations

def device_op(request):
    "do different operation on device folder"
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            if request.POST.get('submit') == 'show':
                folder = "device/" + form.cleaned_data['device'] + "/input/"
                return(redirect(reverse('show_set')+"?folder="+folder))
            if request.POST.get('submit') == 'GetFolderSet':
                folder = DATA_PATH / "device" / form.cleaned_data['device'] / "input/"
                outfold = DATA_PATH / 'tmp'
                Path(outfold).mkdir(exist_ok=True)
                convert2samir(folder, outfold)
                zipfolder(outfold, outfold / "pictset.tar")
                response = FileResponse(open(DATA_PATH / "tmp" / "pictset.tar", 'rb'))
                return response
        mycontext = {'form': form}
        return render (request, 'device_op.html', context=mycontext)
    deviceform = DeviceForm()
    mycontext = {'form': deviceform}
    print(mycontext)
    return render (request, 'device_op.html', context=mycontext)


# process testdata folder set

#IN_FOLDER = BASE_DIR / "testdata" / "wand" / 'exposure'
#IN_FOLDER = BASE_DIR / "testdata" / "wand" / 'zoom'
#IN_FOLDER = BASE_DIR / "testdata" / "wand" / 'plan_zoom'
#IN_FOLDER = BASE_DIR / "testdata" / "wand" / 'plan'
IN_FOLDER = BASE_DIR / "testdata" / "blender" / 'plan'

def process_folder_set(request):
    outpath = DEVICE_PATH / 'folder' / 'input'
    folder = request.GET.get('folder',"testdata/device/serie1/input")
    print("process folder:", folder)
    infolder = BASE_DIR / folder
    if Path.exists(outpath):
        rmtree(outpath, ignore_errors=True)
    Path.mkdir(outpath, parents=True)
    #infolder = IN_FOLDER
    copy_folder_set(infolder, outpath)
    i = 1
    while i<100:
        folder = outpath / str(i)
        if folder.exists():
            receive_scan('folder', folder)
        else:
            break
        i = i+1
    return(redirect(reverse('show_set')+"?folder=device/folder/input"))

# testing

def inference(request):
    if request.method == 'POST':
        form = UploadScanSetFileForm(request.POST, request.FILES)
        if form.is_valid():
            folder = DATA_PATH / 'device' / 'inferencetest' / 'input'
            rmtree(folder, ignore_errors=True)
            Path(folder).mkdir(parents=True, exist_ok=True)
            format_ok = True
            formats = ['.png', 'jpg']
            for file in ['color', 'fringe', 'nolight']:
                if Path(request.FILES[file].name).suffix not in formats:
                    format_ok=False
                else:
                    save_uploaded_file(request.FILES[file], folder / request.FILES[file].name)
                    img2img(folder / request.FILES[file].name, Path(folder / (file +'.png')))
            if format_ok:
                process_3d(folder)
                return HttpResponseRedirect(reverse('show_pictures') +'?folder=device/inferencetest/input/')
            form.add_error(None,'Illegal file formats')
    else:
        form = UploadScanSetFileForm()
    return render (request, 'inference.html', {'form': form})

# callibrations

def calibrate_camera(request):
    deviceid = MYDEVICE
    folder = DATA_PATH / 'device' / deviceid / 'calibrate/calcamera'
    cal_camera(deviceid, Path(folder))
    return HttpResponse("Calibration finish")


####### process scan #######
def proc_scan(request):
    data = DEVICE_PATH / MYDEVICE
    data_path = data / 'input/1/'
    #print(data_path)
    receive_scan(MYDEVICE, data_path)
    return redirect("/test/show_pictures?folder=device/" + MYDEVICE + "/input/1/")

####### receive folder set #######
# copy a folder set and process it with receivescan
#



####### receive folder
#IN_FOLDER = BASE_DIR / "testdata" / "wand" / 'Beige_Toothset' / 'piZ2_210907'
#IN_FOLDER = BASE_DIR / "testdata" / "wand" / 'exposure'

def rec_folder(request, testset=False):
    data = DEVICE_PATH / 'folder' / 'input'
    data_path = data / '1'
    if Path.exists(data):
        rmtree(data, ignore_errors=True)
    Path.mkdir(data, parents=True)
    infolder = IN_FOLDER / '1'
    copy_scan_set(infolder, data_path)
    if testset:
        copy_jpg_test_set(data)
        for i in range(2,6):
            folder = data / str(i)
            receive_scan('folder', folder)
    receive_scan('folder', data_path)
    return redirect("/test/show_pictures?folder=device/folder/input/&number=1")

def rec_folder5(request):
    return rec_folder(request, testset=True)


########### blender #################

TESTDATAFOLDER = BASE_DIR / "testdata" / "render12"
#TESTDATAFOLDER = BASE_DIR / "testdata" / "model.dec" / "render9673"
#TESTDATAFOLDER = BASE_DIR / "testdata" / "device"

def receive_blender(request):
    #print("Start receive blender")
    input_path = DEVICE_PATH / 'blender' / 'input'
    if Path.exists(input_path):
        rmtree(input_path, ignore_errors=True)
    data_path =input_path / '1'
    Path.mkdir(data_path, parents=True)
    infolder = Path(TESTDATAFOLDER)
    #prepare_blender_input(infolder, data_path)
    receive_blender_set(infolder, data_path)
    return redirect(reverse('show_pictures')+"?folder=device/blender/input/1/")

def receive_blender5(request):
    input_path = DEVICE_PATH / 'blender' / 'input'
    if Path.exists(input_path):
        rmtree(input_path, ignore_errors=True)
    data_path =input_path / '1'
    Path.mkdir(data_path, parents=True)
    infolder = Path(TESTDATAFOLDER)

    receive_blender_set(infolder, data_path)

    # folder_path = DEVICE_PATH / 'blender' / 'input'
    # data_path = folder_path / '1'
    # if Path.exists(data_path):
    #     rmtree(data_path, ignore_errors=True)
    # Path.mkdir(data_path, parents=True)
    # infolder = Path(TESTDATAFOLDER)
    # #prepare_blender_input(infolder, data_path)
    # receive_blender_set(infolder, data_path)

    copy_test_set(input_path)
    for i in range(2,6):
        folder = input_path / str(i)
        print( folder )
        process_blender(folder)
    # wait for processing
    return redirect(reverse('show_set')+"?folder=device/blender/input/&number=1")

# def showblender5(request):
#     datapath = 'device/blender/input/'
#     return show5sequense(request, datapath, dias=False)

#################### SCAN ################################

def start_scan(request):
    "Request scan from device and display results"
    #print("Send start scan to device:" + MYDEVICE)
    device_path = "device/" + MYDEVICE + "/input/1/"
    res = send_start_scan()
    if res:
        # wait for processing
        sleep(0.5)
        if NN_ENABLE:
            sleep(8)
        return redirect("/test/show_pictures?folder="+device_path)
    return HttpResponse("Scan start gik galt", res)

def calc_scan(request):
    #device_path = "device/" + MYDEVICE + "/input/1/"
    receive_scan(MYDEVICE, DEVICE_PATH / MYDEVICE / 'input/1/')
    return redirect("/test/show_pictures?folder=device/" + MYDEVICE + "/input/&number=1")

def start_scan5(request):
    "Request scan from device and display results"
    res = send_start_scan()
    if res:
        sleep(11)
        copy_jpg_test_set(DEVICE_PATH / MYDEVICE / 'input')
        for i in range(2,6):
            receive_scan(MYDEVICE, DEVICE_PATH / MYDEVICE / 'input' / str(i))
            #process_scan(MYDEVICE, DEVICE_PATH / MYDEVICE / 'input' / str(i))
        return redirect("/test/show_pictures?folder=device/" + MYDEVICE + "/input/&number=1")
    return HttpResponse("Scan start gik galt", res)

def calc5(request):
    "Request scan from device and display results"
    print("Recalculate 4 pictures:" + MYDEVICE)
    copy_jpg_test_set(DEVICE_PATH / MYDEVICE / 'input')
    device_path = "device/" + MYDEVICE + "/input/1/"
    for i in range(1,6):
        print("Recalculating", DEVICE_PATH / MYDEVICE / 'input' / str(i))
        receive_scan(MYDEVICE, DEVICE_PATH / MYDEVICE / 'input' / str(i))
    return redirect("/test/show_pictures?folder=device/"+device_path)

################## STITCH ################
STITCH_SET = BASE_DIR / "testdata" / "renders211105"
def gen_stitch(request):
    "Stich 2 pcl"
    device = 'stitch'
    ofolder = DEVICE_PATH / device / 'stitch'
    print("Stitch: " + device)
    copy_stitch_test_set(STITCH_SET, ofolder )

    return redirect("/test/show_pictures?folder=device/"+device+"/stitch/&number=1")

def stitch_folder_set(request):
    "stitche standard folder tree"
    gfolder = request.GET.get('folder', 'device/folder/input' )
    folder = DATA_PATH / gfolder
    print ("Stitch input folder", folder)
    number = int(request.GET.get('number', '100') )
    if stitch_run(folder, maxnumber=number):
        return redirect("/test/show_pictures?folder="+gfolder)
    return HttpResponse("No point clouds")

def stitch_model(request):
    "Stitch folder with pointclouds"
    device = 'stitch'
    folder = DEVICE_PATH / device / device
    modelf = request.GET.get('folder', 'testdata/bunny/data' )
    modelfolder = BASE_DIR /  modelf
    read_model_pcl(folder, modelfolder)
    stitch_run(folder)
    return redirect("/test/show_pictures?folder=device/"+device+"/s")

################## Meshing ################
def mesh(request):
    mesh_data = BASE_DIR / "testdata" / "mesh" / "chess.ply"
    device = 'mesh'
    folder = DEVICE_PATH / device / 'mesh'
    rmtree(folder, ignore_errors=True)
    Path.mkdir(folder, parents=True)
    copy2(mesh_data, folder)
    mesh_run(folder)
    return redirect("/test/show_pictures?folder=device/"+device+"/mesh/")

#############  send to live test #################
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
    gen_flash_correction(device)
    #flash_led_test(device)
    return HttpResponse("OK")
