"Filetering utils"
from pathlib import Path
import open3d as o3d
import numpy as np
from stitching.stitch import clean_point_cloud


def scan_filter(filename, outfilename):
    pcl = o3d.io.read_point_cloud(str(Path(filename)))
    new_pcl = clean_point_cloud(pcl)
    #new_pcl = pcl
    print("her")
    o3d.io.write_point_cloud(str(outfilename), new_pcl)

def radius_outliersremoval(infile,outfile):
    pcl = o3d.io.read_point_cloud(str(Path(infile)))
    print("in", len(pcl.points))
    opcl, ind = pcl.remove_radius_outlier(nb_points=16, radius=0.05)
    print(opcl, "Remove", len(ind))
    o3d.io.write_point_cloud(str(outfile), opcl)
    return opcl