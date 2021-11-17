"Display npy"
#from pathlib import Path
import numpy as np
#import open3d as o3d
from matplotlib import pyplot as plt
from matplotlib import use
from matplotlib import style
from mpl_toolkits.mplot3d import axes3d

def show_npy(filename, outputfile=None, grey=False):
    #file = "np/nnunwrap.npy"
    use('Agg')
    db = np.load(filename)
    # print("dtype", db.dtype)
    # print("shape", db.shape)
    # print("ndim", db.ndim)
    # print("min,max", np.amin(db), np.amax(db))
    if True:
        if grey:
            print("min,max", np.min(db), np.max(db) )
            plt.imshow(db, cmap='gray', vmin=0, vmax=1+int(np.max(db)))
            plt.figtext(0.7, 0.8, f"Min: {int(np.min(db))}")
            plt.figtext(0.7, 0.9, f"Max: {int(np.max(db))}")
        else:
            plt.imshow(db)
        #plt.imshow(db, cmap='gray', vmin=0, vmax=54298)
    else:
        xd = []
        yd = []
        zd = []
        for x in range(0,160):
            for y in range (0,160):
                xd.append(x)
                yd.append(y)
                zd.append(db[x][y])
        #print(xd)
        #print(yd)
        #print(zd)
        # setting a custom style to use
        style.use('ggplot')
        # create a new figure for plotting
        fig = plt.figure()
        # create a new subplot on our figure
        # and set projection as 3d
        ax1 = fig.add_subplot(111, projection='3d')
        ax1.set_xlabel('x-axis')
        ax1.set_ylabel('y-axis')
        ax1.set_zlabel('z-axis')
        ax1.scatter(xd, yd, zd, color = 'r', marker = 'o', s=1)
    if outputfile:
        plt.savefig(outputfile)
    #plt.show()
    plt.clf()
