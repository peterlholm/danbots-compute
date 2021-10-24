"""
NN processeing
"""
from pathlib import Path
from shutil import rmtree
from django.shortcuts import redirect, render, HttpResponse
from compute.settings import DATA_PATH, NN_ENABLE  #, API_SERVER, TEMP_PATH
#from nn.inference.config import COLOR_FILENAME, FRINGE_FILENAME, NOLIGHT_FILENAME, MASK_FILENAME
from device.proc import proc_device_data
from .prepare_input import prepare_blender_input, prepare_device_input

# if NN_ENABLE:
#     from nn.inference.process import process_nn_folder
#     from nn.inference.process import process_blender_folder

IN_TESTDATAPATH = Path(__file__).resolve().parent.parent / "testdata"
TESTDATA_OUT = DATA_PATH / 'testdata'

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

def process_blender_testdata(request):
    """
    Process blender testdata set to data/testdata
    """
    TESTDATAFOLDER = Path(__file__).resolve().parent.parent / "testdata/render12"
    data_path = DATA_PATH / 'testdata/process'
    if Path.exists(data_path):
        rmtree(data_path)
    Path.mkdir(data_path)
    infolder = Path(TESTDATAFOLDER)
    if NN_ENABLE:
        process_blender_folder(infolder, data_path)
    return redirect("/nn/show_pictures")
    #return HttpResponse("Testdata Processed...")

def process_device_folder(request):
    """
    Process data in folder from device
    """
    outfolder  = TESTDATA_OUT / 'process'
    rmtree(outfolder, ignore_errors=True)
    copy_devicedata(IN_TESTDATAPATH / "device", outfolder)
    proc_device_data(None, outfolder)
    print("her")
    if NN_ENABLE:
        process_nn_folder(outfolder)
    else:
        print ("NN disabled")
    return redirect("/nn/show_pictures")
