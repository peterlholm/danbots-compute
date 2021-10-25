"preprocess before nn"
from utils.histoimg import histo_img

def preprocessing(folder):
    print("generating histograms")
    histo_img(folder / 'color.jpg', folder / 'color_histo.jpg')
    histo_img(folder / 'color.png', folder / 'color_histo.png')
    histo_img(folder / 'fringe.png', folder / 'fringe_histo.png')
    