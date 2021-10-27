"Simple image manipulations"

from PIL import Image, ImageEnhance

def rotate_img(infile, degree, outfile):
    img = Image.open(infile)
    new = img.rotate(degree, resample=Image.BILINEAR) #resample=Image.BILINEAR
    new.save(outfile)

def change_contrast(infile, outfile, value = 1.5):
    img = Image.open(infile)
    newimage = ImageEnhance.Contrast(img).enhance(value)
    newimage.save(outfile)
    
def change_brightness(infile, outfile, value= 1.5):
    img = Image.open(infile)
    newimage = ImageEnhance.Brightness(img).enhance(value)
    newimage.save(outfile)
  