"stat info for img"
#from pathlib import Path
from matplotlib import pyplot as plt
from matplotlib import use
from PIL import Image, ImageStat

def get_mask(imgfile):
    img = Image.open(imgfile)
    #print("bands", img.getbands())
    mask = img.getchannel('A')
    #mask.show('mask')
    return mask


def histo_img(imgfile, outfile, mask=None):
    use('Agg')
    img = Image.open(imgfile)
    #print("bands", img.getbands())
    # mask = img.getchannel('A')
    # mask.show()
    # imgstat = ImageStat.Stat(img)
    # print("count", imgstat.count)
    grey = img.convert('L')
    #grey.show()
    stat = ImageStat.Stat(grey, mask=mask)
    #print("grey count", stat.count)
    # print("extrema", stat.extrema)
    #print("mean", stat.mean)
    # print("median", stat.median)
    # print("rms", stat.rms)
    # print("var", stat.var)
    # print("stddev", stat.stddev)
    hist = grey.histogram()
    #print(hist)
    X=list(range(0,256))
    # print(len(X))
    # print(len(hist))
    plt.bar(X, hist)
    plt.title("Histogram "+imgfile.name)
    plt.xlabel("Intensity")
    plt.ylabel("Numbers")
    plt.ylim(0,1000)
    plt.figtext(0.7, 0.8, f"mean: {int(stat.mean[0])}")
    plt.figtext(0.7, 0.75, f"rms: {int(stat.rms[0])}")
    plt.figtext(0.7, 0.7, f"count: {int(stat.count[0])}")
    plt.savefig(outfile)
    plt.clf()
    #plt.show()

# file = Path(__file__).resolve().parent.parent / 'testdata' / 'device' / 'color.jpg'
# print ("file", file)
