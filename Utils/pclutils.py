"pointcload utils"
import open3d as o3d
import numpy as np

def mirror(pcloud):
    # mirror x axis
    #print("mirror")
    for p in pcloud.points:
        p[0]= -p[0]
    return

def mirror_file(infile, outfile):
    #print ("proc", infile, outfile)
    pcd = o3d.io.read_point_cloud(str(infile))
    print("in",np.asarray(pcd.points))
    mirror(pcd)
    print("w",np.asarray(pcd.points))
    #print("x", np.asarray(outpcd.points))
    #o3d.io.write_point_cloud(str(outfile), pcd)
    #o3d.io.write_point_cloud("test.ply", outpcd, write_ascii=True)
