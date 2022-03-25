"Convert testset formats"
from os import system
import platform

from pathlib import Path
from shutil import rmtree
from PIL import Image

def img2img(infile, outfile):
    img = Image.open(infile)
    img.save(outfile)

def convert2samir(infolder, outfolder):
    "Convert a device set to samir render format"
    if not Path.exists(infolder):
        raise Exception('no infolder')
    if Path.exists(outfolder):
        rmtree(outfolder, ignore_errors=True)
    Path(outfolder).mkdir()
    i = 1
    while True:
        folder = infolder / str(i)
        if not Path(folder).exists():
            break
        ofold = Path(outfolder) / ('render'+str(i-1))
        Path(ofold).mkdir()
        img2img(Path(folder) / 'color.jpg',  Path(ofold) / 'image8.png')
        img2img(Path(folder) / 'dias.jpg',  Path(ofold) / 'image0.png')
        img2img(Path(folder) /'nolight.jpg',  Path(ofold) /'image9.png')
        i +=1

def zipfolder(infolder, outfolder):
    if platform.system() == "Windows":
        cmd = "tar -c -f " + str(Path(outfolder)) + " -C " + str(infolder) + " . "
    else:
        cmd ="tar -cf " + str(Path(outfolder)) + " -C " + str(infolder) + " . "
    res = system(cmd)
    return res

if __name__ == "__main__":
    _BASE = Path(__file__).parent.parent
    infold = Path('../testdata/device/serie1/input')
    outfold = _BASE / '../data/testout'
    print("Convert from " + str(infold) + " to " + str(outfold))
    convert2samir(infold, outfold)
    outfil = Path('./out.tar')
    zipfolder(infold, outfil)
