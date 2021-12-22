# module for light compensation
# genrating maps:
#   gen_image_diff_map: generate a map with difference for picels compared to meadia picture value
#   gen_image_mult_map: generate a map with multifier for picels compared to meadia picture value
# picture correction:
#   apply_image_diff_map: apply the diff map on the given picture
#   apply_image_mult_map: apply the mult map on the given picture

from pathlib import Path
from PIL import Image, ImageStat, ImageFilter
import numpy as np

_DEBUG = True
COMP_OFFSET = 200
MEDIAN_FILTER_SIZE = 7

def gen_image_diff_map(inpicture, outdiffmap):
    outmap = Path(outdiffmap)
    img = Image.open(Path(inpicture))
    imgstat = ImageStat.Stat(img)
    grey = img.convert('L')
    stat = ImageStat.Stat(grey)
    mean = stat.mean[0]
    if _DEBUG:
        print("Image Mean:", imgstat.mean, "extrema:", imgstat.extrema, "Stdv:", imgstat.stddev)
        print("Grey Mean:", mean, "extrema:", stat.extrema, "Stdv:", stat.stddev)
    imean = int(mean)
    korr = Image.new('L', grey.size)
    np_korr = np.empty((grey.width, grey.height), dtype=np.byte)
    if MEDIAN_FILTER_SIZE != 0:
        korr1 = korr.filter(ImageFilter.MedianFilter(size=MEDIAN_FILTER_SIZE))
        korr = korr1
    for x in range(0, grey.width):
        for y in range(0, grey.height):
            cor = imean - grey.getpixel((x,y))
            np_korr[x,y] = cor
            if _DEBUG:
                val = cor + COMP_OFFSET
                korr.putpixel((x,y), val )
    if _DEBUG:
        korr.save(outdiffmap.with_suffix('.png'))
    np.save(outmap, np_korr)

def gen_image_mult_map(inpicture, outdiffmap):
    outmap = Path(outdiffmap)
    img = Image.open(Path(inpicture))
    imgstat = ImageStat.Stat(img)
    grey = img.convert('L')
    stat = ImageStat.Stat(grey)
    mean = stat.mean[0]
    if _DEBUG:
        print("Image Mean:", imgstat.mean, "extrema:", imgstat.extrema, "Stdv:", imgstat.stddev)
        print("Grey Mean:", mean, "extrema:", stat.extrema, "Stdv:", stat.stddev)
    imean = int(mean)
    korr = Image.new('L', grey.size)
    np_korr = np.empty((grey.width, grey.height), dtype=np.float32)
    if MEDIAN_FILTER_SIZE != 0:
        korr1 = korr.filter(ImageFilter.MedianFilter(size=MEDIAN_FILTER_SIZE))
        korr = korr1
    for x in range(0, grey.width):
        for y in range(0, grey.height):
            cor = imean - grey.getpixel((x,y))
            np_korr[x,y] = cor
            if _DEBUG:
                val = cor + COMP_OFFSET
                korr.putpixel((x,y), val )
    if _DEBUG:
        korr.save(outdiffmap.with_suffix('.png'))
    np.save(outmap, np_korr)

def apply_image_diff_map(image, map, outimage):
    outimage = Path(outimage)
    img = Image.open(image)
    np_corr = np.load(map)
    #kor = Image.open(korr)
    print (img.mode)
    for x in range(0, img.width):
        for y in range(0, img.height):
            #comp = kor.getpixel((x,y)) - COMP_OFFSET
            comp = np_corr[x,y]
            val = img.getpixel((x,y))
            val2 = (val[0]+comp, val[1]+comp, val[2]+comp, val[3])
            img.putpixel((x,y), val2 )
    img.save(outimage)
   

def gen_dias_correction(inpicture, outfolder):
    # generate a diff and a mult correction matrix for a total white image
    #MEDIAN_FILTER_SIZE = 3 # 7, 31
    COMP_OFFSET = 200
 
    outfolder = Path(outfolder)
    img = Image.open(inpicture)
    if _DEBUG:
        print("Input:", img.size, img.mode)
    grey = img.convert('L')
    mean = ImageStat.Stat(grey).mean[0]
    print ("Mean:", mean)
    imean = int(mean)
    korr = Image.new('L', grey.size)
    for x in range(0, grey.width):
        for y in range(0, grey.height):
            val = imean - grey.getpixel((x,y)) + COMP_OFFSET
            korr.putpixel((x,y), val )
    korr.save(outfolder / "diff.png")
    korr1 = korr.filter(ImageFilter.MedianFilter(size=MEDIAN_FILTER_SIZE))
    korr1.save(outfolder / "korr_diff.png")

    np_korr = np.empty((grey.width, grey.height), dtype=np.float32)
    for x in range(0, grey.width):
        for y in range(0, grey.height):
            cor = grey.getpixel((x,y))/mean
            np_korr[x,y] = cor
            val = cor * 10 + COMP_OFFSET
            korr.putpixel((x,y), int(val) )
    np.save (outfolder / "korr.npy" , np_korr)
    korr.save(outfolder / "mult.png")
    korr1 = korr.filter(ImageFilter.MedianFilter(size=MEDIAN_FILTER_SIZE))
    korr1.save(outfolder / "korr_mult.png")

def apply_diff(image, korr, outfolder):
    outfolder = Path(outfolder)
    img = Image.open(image)
    kor = Image.open(korr)
    print (img.mode)
    for x in range(0, img.width):
        for y in range(0, img.height):
            comp = kor.getpixel((x,y)) - COMP_OFFSET
            val = img.getpixel((x,y))
            val2 = (val[0]+comp, val[1]+comp, val[2]+comp, val[3])
            img.putpixel((x,y), val2 )
    img.save(outfolder / "new_diff.png")

def apply_mult(image, korr, outfolder):
    outfolder = Path(outfolder)
    img = Image.open(image)
    kor = Image.open(korr)
    print (img.mode)
    for x in range(0, img.width):
        for y in range(0, img.height):
            corr= (kor.getpixel((x,y)) - COMP_OFFSET)/10.0
            print ("corr", corr)
            val = img.getpixel((x,y))
            val2 = (int(val[0]/corr), int(val[1]/corr), int(val[2]/corr), val[3])
            img.putpixel((x,y), val2 )
    img.save(outfolder / 'new_mult.png')

def apply_np_mult(image, korr, outfolder):
    outfolder = Path(outfolder)
    img = Image.open(image)
    kor = np.load(korr)
    print (img.mode)
    for x in range(0, img.width):
        for y in range(0, img.height):
            corr= kor[x,y]
            print ("corr", corr)
            val = img.getpixel((x,y))
            val2 = (int(val[0]/corr), int(val[1]/corr), int(val[2]/corr), val[3])
            img.putpixel((x,y), val2 )
    img.save(outfolder / 'new_mult.png')


if __name__ == '__main__':
    picture = Path(__file__).parent / "pic" / "1.png"
    #gen_image_diff_map(picture, Path('out') / 'diff_map.npy')
    #apply_image_diff_map(picture, Path('out') / 'diff_map.npy', Path('out') / 'new_diff_image.png')

    gen_dias_correction(picture,'out')

    #apply_diff(picture, 'out/korr_diff.png', 'out')
    
    apply_mult(picture, 'out/korr_mult.png', 'out')

    #apply_np_mult(picture, 'out/korr.npy', 'out')