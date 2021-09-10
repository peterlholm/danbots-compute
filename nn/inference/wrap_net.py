from pathlib import Path
from nn.inference.config import COLOR_FILENAME, NOLIGHT_FILENAME
from nn.inference.create_mask import create_mask
import time

def process_net(folder):
    start = time.time()
    infolder = Path(folder)
    create_mask(infolder / COLOR_FILENAME, infolder / NOLIGHT_FILENAME, folder)
    #mask(folder)
    #nn_h_process(folder)
    end = time.time()
    print('Wrap_net Processing time  {:.2f} sec'.format(end-start))
    return
