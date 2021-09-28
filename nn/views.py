from pathlib import Path
from shutil import rmtree
from django.shortcuts import render, HttpResponse
from compute.settings import DATA_PATH, NN_ENABLE  #, API_SERVER, TEMP_PATH
from nn.inference.config import *
if NN_ENABLE:
    from nn.inference.process import process_blender_folder

TESTDATAPATH = Path(__file__).resolve().parent.parent / "testdata/render12"

def index(request):
    return render (request, 'nn_index.html')

def process_testdata(request):
    data_path = DATA_PATH / 'testdata'
    if Path.exists(data_path):
        rmtree(data_path)
    Path.mkdir(data_path)
    infolder = Path(TESTDATAPATH)
    if NN_ENABLE:
        process_blender_folder(infolder, data_path)
    return HttpResponse("Processing...")

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
