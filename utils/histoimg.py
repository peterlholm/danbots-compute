"stat info for img"
from pathlib import Path
from matplotlib import pyplot as plt
from PIL import Image, ImageStat

def histo_img(imgfile, outfile):
    img = Image.open(imgfile)
    grey = img.convert('L')
    stat = ImageStat.Stat(grey)
    # print("extrema", stat.extrema)
    # print("mean", stat.mean)
    # print("median", stat.median)
    # print("rms", stat.rms)
    # print("var", stat.var)
    # print("stddev", stat.stddev)
    hist = grey.histogram()
    X=list(range(0,256))
    # print(len(X))
    # print(len(hist))
    plt.bar(X, hist)
    plt.title("Histogram")
    plt.xlabel("Intensity")
    plt.ylabel("Numbers")
    plt.text(200,200,f"mean: {int(stat.mean[0])}")
    plt.text(200,230,f"rms: {int(stat.rms[0])}")
    plt.savefig(outfile)
    plt.show()

# file = Path(__file__).resolve().parent.parent / 'testdata' / 'device' / 'color.jpg'
# print ("file", file)
