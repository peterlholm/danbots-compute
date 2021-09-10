import os
from pathlib import Path
from PIL import Image


COLORPICTURE = "image8.png"
BLACKWHITEPICTURE = "image8.png"
DIASPICTURE = "image0.png"
NOLIGHT = "image9.png"

OUTCOLOR = "color.png"
OUTDIAS = "dias.png"
OUTNOLIGHT = "nolight.png"

def convert_from_blender(infolder, outfolder):
    pic = Image.open(infolder / COLORPICTURE)
    pic.save(Path(outfolder) / OUTCOLOR)
    pic = Image.open(infolder / DIASPICTURE)
    pic.save(Path(outfolder) / OUTDIAS)
    pic = Image.open(infolder / NOLIGHT)
    pic.save(Path(outfolder) / OUTNOLIGHT)
    return

def traverse_folder(intree, outtree):
    print("Converting Blender folder " + str(intree) + " to " + str(outtree))
    if not Path.exists(intree):
        print ("Input directory does not exist: " + str(intree))
        raise Exception("Input directory does not exist", intree)
        return False
    os.makedirs(outtree) 
    no = 0
    while True:
        indir = intree / ("render" + str(no))
        if Path.exists(indir):
            outdir = Path(outtree) / str(no)
            os.makedirs(outdir)
            convert_from_blender(indir, outdir)
        else:
            break
        no += 1
        if no % 10 == 0:
            print(".", end='')
    print("")
    return


# infolder = Path('C:\\Peter\\danbots\\pictures\\blender\\bridge1scans')
# outfolder = 'pic'
# #export_from_blender(infolder,outfolder)

# traverse_folder(infolder, 'pic\\test')
