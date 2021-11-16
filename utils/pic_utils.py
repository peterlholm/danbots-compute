"Utillities for picture management"
from PIL import Image

def create_mask(img, mask):
    mask = Image.new('L', img.size, color=0)
    for x in range(20, img.width-30):
        for y in range(10, img.height-17):
            mask.putpixel((x,y), 255)
    return mask

def insert_mask(infile, mask, outfile):
    "mask is (left,top,right,button)"
    #print(infile)
    img = Image.open(infile)
    #img.show()
    maskimg = Image.new('L', img.size, color=0)
    for x in range(mask[0], mask[2]):
        for y in range(mask[1], mask[3]):
            maskimg.putpixel((x,y), 255)
    img.putalpha(maskimg)
    #img.show()
    img.save(outfile)

def include_device_masks(file, mask):
    print(file)
    img = Image.open(file)
    img.show()
    maskimg = Image.new('L', img.size, color=0)
    for x in range(mask[0], mask[2]):
        for y in range(mask[1], mask[3]):
            maskimg.putpixel((x,y), 255)
    img.putalpha(maskimg)
    img.show()
    img.save("myfile.png")

def include_pic_mask(pic_filename, mask_filename, out_filename):
    _img = Image.open(pic_filename)
    _mask= Image.open(mask_filename)
    for x in range(0, _img.width):
        for y in range(0, _img.height):
            if _mask.getpixel==0:
                _img.putpixel((x,y),(0,0,0,255))
    _img.save(out_filename)

def include_all_masks(folder):
    print(str(folder))
    mask = (30,30,100,100)
    include_device_masks(folder / '1' / 'dias.jpg', mask)

def convert_mask_to_color(picture_filename, out_filename, color=0):
    _img = Image.open(picture_filename)
    for x in range(0, _img.width):
        for y in range(0, _img.height):
            pixcel = _img.getpixel((x,y))
            if pixcel[3]==0:
                _img.putpixel((x,y),(color,color,color,0))
    _img.save(out_filename)
