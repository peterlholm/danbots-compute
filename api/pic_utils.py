"""Utillities for picture management"""
from PIL import Image

def create_mask(img, mask):
    mask = Image.new('L', img.size, color=0)
    for x in range(20, img.width-30):
        for y in range(10, img.height-17):
            mask.putpixel((x,y), 255)
    return mask

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

def include_all_masks(folder):
    print(str(folder))
    mask = (30,30,100,100)
    include_device_masks(folder / '1' / 'dias.jpg', mask)
