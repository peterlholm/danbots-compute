"""
flash test
"""
from pathlib import Path
from PIL import Image, ImageStat, ImageFilter # ImageEnhance,


folder = "calibrate/testdata/"
filename = "flash01.jpg"

file = Path(folder+filename)

def flash_led_test():
    img = Image.open(file)
    grey = img.convert('L')

    print(img.getbands())
    print(img.size) #width height
    width = img.width
    height = img.height

    reduce = 0.30
    rect = (width*reduce/2, height*reduce/2, width*(1-reduce/2), height*(1-reduce/2))
    crop = grey.crop(rect)
    #crop.show()

    small = crop.reduce(8)
    small.show()

    histo = small.histogram()
    print(histo)
    
    stat = ImageStat.Stat(small)
    mean = int(stat.mean[0])
    print ("mean", mean)
    korr = Image.new('L', small.size)

    for x in range(0, korr.width):
        for y in range(0, korr.height):
            val = mean - small.getpixel((x,y)) + 200
            #print(val)
            korr.putpixel((x,y), val )

    #korr.show()

    blur = korr.filter(ImageFilter.BLUR)

    #blur.show()

    bblur = korr.filter(ImageFilter.BoxBlur(10))
    bblur.show()

    repair = Image.new('L', small.size)

    for x in range(0, repair.width):
        for y in range(0, repair.height):
            val = small.getpixel((x,y)) + (bblur.getpixel((x,y)) - 200)
            #print(val)
            repair.putpixel((x,y), val )

    repair.show()


    stat = ImageStat.Stat(crop)
    print ("count",stat.count)
    print ("sum",stat.sum)
    print ("sum2",stat.sum2)
    print ("mean",stat.mean)
    print ("rms",stat.rms)
    print ("var",stat.var)
    print ("stddev",stat.stddev)

    #img.show()
    #grey.show()
