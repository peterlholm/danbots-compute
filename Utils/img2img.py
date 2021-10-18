from PIL import Image

def img2img(infile, outfile):
    img = Image.open(infile)
    img.save(outfile)
    