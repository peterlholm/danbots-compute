from pathlib import Path
from PIL import Image, ImageEnhance, ImageStat




folder = "testdata/"
filename = "color.jpg"

file = Path(folder+filename)

img = Image.open(file)
grey = img.convert('L')

print(img.getbands())
print(img.size) #width height

histo = img.histogram()

stat = ImageStat.Stat(img)

print (stat)

img.show()
grey.show()
