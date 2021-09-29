"""
NN processeing
"""
from pathlib import Path
from shutil import rmtree
from django.shortcuts import redirect, render, HttpResponse
from compute.settings import DATA_PATH, NN_ENABLE  #, API_SERVER, TEMP_PATH
from nn.inference.config import COLOR_FILENAME, FRINGE_FILENAME, NOLIGHT_FILENAME, MASK_FILENAME
from device.proc import proc_device_data
from .prepare_input import prepare_blender_input, prepare_device_input

if NN_ENABLE:
    from nn.inference.process import process_nn_folder
    from nn.inference.process import process_blender_folder

IN_TESTDATAPATH = Path(__file__).resolve().parent.parent / "testdata"
TESTDATA = DATA_PATH / 'testdata'

print(IN_TESTDATAPATH)

def copy_testdata(infolder, outfolder):
    if not Path.exists(infolder):
        raise Exception("infolder not found " + str(infolder))
    if Path.exists(outfolder):
        raise Exception("Outfolder already exist " + str(outfolder))
    Path.mkdir(outfolder)
    prepare_blender_input(infolder, outfolder)

    return True

def copy_devicedata(infolder, outfolder):
    if not Path.exists(infolder):
        raise Exception("infolder not found " + str(infolder))
    if Path.exists(outfolder):
        raise Exception("Outfolder already exist " + str(outfolder))
    Path.mkdir(outfolder)
    prepare_device_input(infolder, outfolder)

    return True

def index(request):
    return render (request, 'nn_index.html')

def process_device_folder(request):
    outfolder  = TESTDATA / 'process'
    rmtree(outfolder, ignore_errors=True)
    copy_devicedata(IN_TESTDATAPATH / "device", outfolder)
    proc_device_data(None, outfolder)
    print("her")
    if NN_ENABLE:
        process_nn_folder(outfolder)
    else:
        print ("NN disabled")
    return redirect("/nn/show_pictures")

def process_folder(request):
    outfolder  = TESTDATA / 'process'
    rmtree(outfolder, ignore_errors=True)
    copy_testdata(IN_TESTDATAPATH / "device", outfolder)
    proc_device_data(None, outfolder)
    if NN_ENABLE:
        process_nn_folder(outfolder)
    else:
        print ("NN disabled")
    return redirect("/nn/show_pictures")
    #return HttpResponse("Folder processed")


def process_testdata(request):
    TESTDATAFOLDER = Path(__file__).resolve().parent.parent / "testdata/render12"
    data_path = DATA_PATH / 'testdata'
    if Path.exists(data_path):
        rmtree(data_path)
    Path.mkdir(data_path)
    infolder = Path(TESTDATAFOLDER)
    if NN_ENABLE:
        process_blender_folder(infolder, data_path)

    return HttpResponse("Testdata Processed...")

def showresult(request):
    path = '/data/testdata/'
    picpath = request.GET.get('folder', path)

    piclist = [picpath + COLOR_FILENAME,
        picpath + FRINGE_FILENAME,
        picpath + NOLIGHT_FILENAME,
        picpath + MASK_FILENAME,
        picpath + "nnwrap1.png",
        picpath + "nnunwrap.png",
        picpath + "nndepth.png",
        picpath + "nndepth2.png",
      ]
    mycontext = {
        'path': picpath,
        'pictures': piclist,
        'pic1': picpath + "color.png",
        'pic2': picpath + "dias.png",
        'pic3': picpath + "nolight.png",
        'pic4': picpath + "mask.png",
        'pic5': picpath + "nnwrap1.png",
        'pic6': picpath + "nnunwrap.png",
        'pic7': picpath + "nndepth.png",
        # 'pic8': picpath + "unwrap1.png"
        #'pic8': picpath + "../testdata/"
    }
    return render (request, 'showresult.html', context=mycontext)

def show_pictures(request):
    datapath = 'testdata/process/'
    abs_path = DATA_PATH / request.GET.get('folder', datapath)
    pic_list = []
    for p in Path.glob(abs_path,"*.jpg"):
        pic_list.append("/data/"+datapath+p.name)
    for p in Path.glob(abs_path,"*.png"):
        pic_list.append("/data/"+datapath+p.name)
    mycontext={"path": datapath, "pictures": pic_list}
    return render (request, 'showresult.html', context=mycontext)
