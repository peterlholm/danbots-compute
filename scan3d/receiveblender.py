"Process a blender dataset"
from pathlib import Path
#from shutil import copy2
from PIL import Image
from scan3d.nn.inference.config import COLOR_FILENAME,FRINGE_FILENAME,NOLIGHT_FILENAME
from scan3d.nn.inference.process_input import process_input_folder
from .preprocessing import preprocessing
# def process_blender_testdata(request):
#     """
#     Process blender testdata set to data/testdata
#     """
#     TESTDATAFOLDER = Path(__file__).resolve().parent.parent / "testdata/render12"
#     data_path = DATA_PATH / 'testdata/process'
#     if Path.exists(data_path):
#         rmtree(data_path)
#     Path.mkdir(data_path)
#     infolder = Path(TESTDATAFOLDER)
#     if NN_ENABLE:
#         process_blender_folder(infolder, data_path)
#     return redirect("/nn/show_pictures")
#     #return HttpResponse("Testdata Processed...")

# blender names

COLORPICTURE = "image8.png"
BLACKWHITEPICTURE = "image8.png"
DIASPICTURE = "image0.png"
NOLIGHT = "image9.png"


# OUTCOLOR = "color.png"
# OUTDIAS = "dias.png"
# OUTNOLIGHT = "nolight.png"

def prepare_blender_input(infolder, outfolder=None):
    if not outfolder:
        outfolder = infolder
    pic = Image.open(infolder / COLORPICTURE)
    pic.save(Path(outfolder) / COLOR_FILENAME)
    pic = Image.open(infolder / DIASPICTURE)
    pic.save(Path(outfolder) / FRINGE_FILENAME)
    pic = Image.open(infolder / NOLIGHT)
    pic.save(Path(outfolder) / NOLIGHT_FILENAME)

def receive_scan_set(folder):
    print("Receive Blender Scan_set", folder)
    preprocessing(folder)
    process_input_folder(folder)

    # if Path.exists(folder / 'pointcloud.jpg'):
    #     copy2(folder / 'pointcloud.jpg', DEVICE_PATH / deviceid / 'input' / 'last_dias.jpg' )
