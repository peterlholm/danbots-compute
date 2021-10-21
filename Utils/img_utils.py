"Simple image manipulations"

from PIL import Image

def rotate_img(infile, degree, outfile):
    img = Image.open(infile)
    new = img.rotate(degree, resample=Image.BILINEAR) #resample=Image.BILINEAR
    new.save(outfile)
