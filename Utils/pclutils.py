"pointcload utils"
import open3d as o3d
import numpy as np

# virker ikke af en eller anden grund
# def mirror(pcloud):
#     # mirror x axis
#     #print("mirror")
#     for p in pcloud.points:
#         p[0]= -p[0]
#     return

# def mirror_file(infile, outfile):
#     #print ("proc", infile, outfile)
#     pcd = o3d.io.read_point_cloud(str(infile))
#     print("in",np.asarray(pcd.points))
#     mirror(pcd)
#     print("w",np.asarray(pcd.points))
#     #print("x", np.asarray(outpcd.points))
#     #o3d.io.write_point_cloud(str(outfile), pcd)
#     #o3d.io.write_point_cloud("test.ply", outpcd, write_ascii=True)

def mirror_pcl(infile, outfile):
    pcd = o3d.io.read_point_cloud(str(infile))
    arr = np.asarray(pcd.points)
    #print('xyz_load', arr)
    for pkt in arr:
        pkt[0] = -pkt[0]
    #print('xyz_load', arr)
    opcd = o3d.geometry.PointCloud()
    opcd.points = o3d.utility.Vector3dVector(arr)
    o3d.io.write_point_cloud(str(outfile), opcd)
