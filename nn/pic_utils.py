from PIL import Image, ImageStat

def get_brightness(picture):
    image = Image.open(picture)
    greyscale_image = image.convert('L')
    histogram = greyscale_image.histogram()
    print(histogram)
    pixels = sum(histogram)
    brightness = scale = len(histogram)

    for index in range(0, scale):
        ratio = histogram[index] / pixels
        brightness += ratio * (-scale + index)

    return 1 if brightness == 255 else brightness / scale


def get_stats(picture):
    image = Image.open(picture)
    stats = ImageStat.Stat(image)

    print("Extrema",stats.extrema)
    print("Count", stats.count)
    print("Sum", stats.sum)
    print("Sum2", stats.sum2)
    print("Mean", stats.mean)
    print("Median", stats.median)
    print("Rms", stats.rms)
    print("Var", stats.var)
    print("Stddev", stats.stddev)

FIL = "../tmp/dias.png"

# j = get_brightness(fil)
# print ("Brightness", j)

get_stats(FIL)
