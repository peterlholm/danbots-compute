"Common processing"
#from os import path
from pathlib import Path
from shutil import copy2, rmtree
#from compute.settings import BASE_DIR
#from scan3d.nn.inference.config import FRINGE_FILENAME
from utils.histoimg import histo_img
from utils.img_utils import change_contrast, change_brightness
from utils.pcl_utils import ply2jpg, mirror_pcl #, pcl2jpg
#from PIL import Image

_DEBUG=False

def copy_jpg_test_set(folder):
    path1 = folder / '1'
    for i in range(2,6):
        newpath = folder / str(i)
        rmtree(newpath, ignore_errors=True)
        Path(newpath).mkdir()
        copy2(path1 / 'color.jpg', newpath / 'color.jpg')
        #copy2(path1 / 'dias.jpg', newpath / 'dias.jpg')
        copy2(path1 / 'nolight.jpg', newpath / 'nolight.jpg')
    change_contrast(folder / '1' / 'dias.jpg', folder / '2' / 'dias.jpg', 0.8)
    change_contrast(folder / '1' / 'dias.jpg', folder / '3' / 'dias.jpg', 1.2)
    change_brightness(folder / '1' / 'dias.jpg', folder / '4' / 'dias.jpg', 0.8)
    change_brightness(folder / '1' / 'dias.jpg', folder / '5' / 'dias.jpg', 1.2)

def copy_test_set(folder):
    path1 = folder / '1'
    for i in range(2,6):
        newpath = folder / str(i)
        rmtree(newpath, ignore_errors=True)
        Path(newpath).mkdir()
        copy2(path1 / 'fringe.png', newpath / 'fringe.png')
        copy2(path1 / 'color.png', newpath / 'color.png')
        copy2(path1 / 'nolight.png', newpath / 'nolight.png')
    change_contrast(folder / '1' / 'fringe.png', folder / '2' / 'fringe.png', 0.8)
    change_contrast(folder / '1' / 'fringe.png', folder / '3' / 'fringe.png', 1.2)
    change_brightness(folder / '1' / 'fringe.png', folder / '4' / 'fringe.png', 0.8)
    change_brightness(folder / '1' / 'fringe.png', folder / '5' / 'fringe.png', 1.2)

def copy_stitch_test_set(from_folder, to_folder):
    #STITCH_SET = BASE_DIR / "testdata" / "renders211105" / "render14"
    #TESTDATAFOLDER = BASE_DIR / "testdata" / "renders211105" / "render23044"
    Path(to_folder).mkdir(parents=True, exist_ok=True)
    for i in range(1,50):
        ifold = from_folder / ('render'+str(i-1))
        ofold = to_folder / str(i)
        #print(ifold)
        if Path(ifold).exists():
            Path(ofold).mkdir(parents=True, exist_ok=True)
            copy2(ifold / "image8.png", ofold / "color.png")
            copy2(ifold / "pointcl-nndepth.ply", ofold / "pointcl-nndepth.ply")
            mirror_pcl(ofold / "pointcl-nndepth.ply", ofold / 'pointcloud.ply')
            #filter_pcl(folder / 'pointcloud.ply', folder / 'pointcloud1.ply')
            #mask_pcl(folder / 'pointcloud.ply', folder / 'mask.npy', folder / 'nypointcloud.ply')
            ply2jpg(ofold / 'pointcloud.ply', ofold / 'pointcloud.jpg')
            #ply2jpg(ofold / 'pointcloud1.ply', ofold / 'pointcloud1.jpg')

def general_postprocessing(folder):
    "preproccsing for scan and blender"
    if _DEBUG:
        histo_img(folder / 'color.png', folder / 'color_histo.png')
        histo_img(folder / 'fringe.png', folder / 'fringe_histo.png')
        #histo_img(folder / 'nolight.png', folder / 'nolight_histo.png')
