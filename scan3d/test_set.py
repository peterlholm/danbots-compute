"Common processing"
from pathlib import Path
from shutil import copy2, rmtree
from utils.img_utils import change_contrast, change_brightness
from utils.pcl_utils import ply2jpg, mirror_pcl #, pcl2jpg
from utils.img2img import img2jpg

_DEBUG=False

CONTRAST_LOW = 0.5
CONTRAST_HIGH = 1.5
BRIGHTNESS_LOW = 0.5
BRIGHTNESS_HIGH = 1.5

def copy_scan_set(infolder, outfolder):
    if not outfolder.exists():
        Path(outfolder).mkdir(exist_ok=True)
    copy2(infolder / 'color.jpg', outfolder / 'color.jpg')
    copy2(infolder / 'dias.jpg', outfolder / 'dias.jpg')
    copy2(infolder / 'nolight.jpg', outfolder / 'nolight.jpg')

def copy_folder_set(infolder, outfolder):
    "Copy org picture from folder set"
    if _DEBUG:
        print("copy_folder_set ",infolder, outfolder)
    Path(outfolder.parent / 'device_config.conf').unlink(missing_ok=True)
    if Path(infolder / 'device_config.conf').exists():
        copy2(infolder / 'device_config.conf', outfolder.parent / 'device_config.conf')
    i = 1
    while i<100:
        inpath = infolder / str(i)
        if not inpath.exists():
            break
        outpath = outfolder / str(i)
        copy_scan_set(inpath,outpath)
        i = i+1

def copy_jpg_test_set(folder):
    path1 = folder / '1'
    for i in range(2,6):
        newpath = folder / str(i)
        rmtree(newpath, ignore_errors=True)
        Path(newpath).mkdir()
        copy2(path1 / 'color.jpg', newpath / 'color.jpg')
        #copy2(path1 / 'dias.jpg', newpath / 'dias.jpg')
        copy2(path1 / 'nolight.jpg', newpath / 'nolight.jpg')
    change_contrast(folder / '1' / 'dias.jpg', folder / '2' / 'dias.jpg', CONTRAST_LOW)
    change_contrast(folder / '1' / 'dias.jpg', folder / '3' / 'dias.jpg', CONTRAST_HIGH)
    change_brightness(folder / '1' / 'dias.jpg', folder / '4' / 'dias.jpg', BRIGHTNESS_LOW)
    change_brightness(folder / '1' / 'dias.jpg', folder / '5' / 'dias.jpg', BRIGHTNESS_HIGH)

def copy_test_set(folder):
    """Copy png /1 to 4 new folders"""
    path1 = folder / '1'
    for i in range(2,6):
        newpath = folder / str(i)
        rmtree(newpath, ignore_errors=True)
        Path(newpath).mkdir()
        copy2(path1 / 'fringe.png', newpath / 'fringe.png')
        copy2(path1 / 'color.png', newpath / 'color.png')
        copy2(path1 / 'nolight.png', newpath / 'nolight.png')
    change_contrast(folder / '1' / 'fringe.png', folder / '2' / 'fringe.png', CONTRAST_LOW)
    change_contrast(folder / '1' / 'fringe.png', folder / '3' / 'fringe.png', CONTRAST_HIGH)
    change_brightness(folder / '1' / 'fringe.png', folder / '4' / 'fringe.png', BRIGHTNESS_LOW)
    change_brightness(folder / '1' / 'fringe.png', folder / '5' / 'fringe.png', BRIGHTNESS_HIGH)

def copy_stitch_test_set(from_folder, to_folder):
    #STITCH_SET = BASE_DIR / "testdata" / "renders211105" / "render14"
    #TESTDATAFOLDER = BASE_DIR / "testdata" / "renders211105" / "render23044"
    Path(to_folder).mkdir(parents=True, exist_ok=True)
    for i in range(1,20):
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

def rename_blender_files_set(from_folder):
    for i in range(1,20):
        #ifold = from_folder / ('render'+str(i-1))
        ifold = from_folder / (str(i))
        #ofold = to_folder / str(i)
        #print(ifold)
        if Path(ifold).exists():
            img2jpg(ifold / "image8.png", ifold / "color.jpg")
            img2jpg(ifold / "image0.png", ifold / "dias.jpg")
            img2jpg(ifold / "image9.png", ifold / "nolight.jpg")
