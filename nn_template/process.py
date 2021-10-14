"""Module for processing one picture set"""
from pathlib import Path
from compute.settings import DATA_PATH

MODEL_PATH = DATA_PATH / 'nnmodels/'
# input
FRINGE_PICTURE = 'fringe.png'
COLOR_PICTURE = 'color.png'
NOLIGHT_PICTURE = 'nolight.png'
# output
P_CLOUD_FILENAME = 'pointcloud.ply'

L_MODEL = MODEL_PATH / 'L_model.h5'
H_MODEL = MODEL_PATH / 'H_model.h5'

_DEBUG = True

def process_picture_set(folder):
    """
    Process the pictures in the folder
    folder : Path
    """
    p_folder = Path(folder)
    color_picture = p_folder / COLOR_PICTURE
    fringe_picture = p_folder / FRINGE_PICTURE
    nolight_picture = p_folder / NOLIGHT_PICTURE

    if _DEBUG:
        print("Processing folder:", p_folder)
        print("Pictures:", color_picture, fringe_picture, nolight_picture)
        print("Model Path:", MODEL_PATH)

    #step1(p_folder)
    #step2(p_folder)

    if _DEBUG:
        print("PointCloud generated", folder / P_CLOUD_FILENAME)
    result = True
    return result
