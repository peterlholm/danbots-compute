"module for converting images"
from PIL import Image

def img2img(infile, outfile):
    img = Image.open(infile)
    img.save(outfile)

def img2jpg(infile, outfile):
    img = Image.open(infile)
    img2 = img.convert("RGB")
    img2.save(outfile)
