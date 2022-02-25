from pathlib import Path
import numpy as np
import open3d as o3d
from utils.pcl_utils import pcl2jpg

def bpa(pcd):
    distances = pcd.compute_nearest_neighbor_distance()
    avg_dist = np.mean(distances)
    radius = 3 * avg_dist
    print("Radius", radius)
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd, o3d.utility.DoubleVector([radius, radius * 2]))
    print(mesh)
    return radius

def poisson_reconstruction(pcd):
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=8, width=0, scale=1.1, linear_fit=False)[0]

    bbox = pcd.get_axis_aligned_bounding_box()
    p_mesh_crop = mesh.crop(bbox)

    return p_mesh_crop
    

def mesh_run(folder):
    filename = "chess.ply"
    file = Path(folder) / filename
    pcl =o3d.io.read_point_cloud(str(file))
    outfile = Path(folder) / "pic1.jpg"
    pcl2jpg(pcl, outfile)
    print("Number of points: ", len(pcl.points))
    print("Downsample the point cloud with a voxel of 0.05")
    downpcd = pcl.voxel_down_sample(voxel_size=0.5)
    pcl2jpg(downpcd, Path(folder) / "pic2.jpg")
    outfile = Path(folder) / "pic2.ply"
    print("Number of downsampled points: ", len(downpcd.points))

    o3d.io.write_point_cloud(str(outfile), downpcd)
    #bpa(downpcd)
    stlimg = poisson_reconstruction(downpcd)
    return
    
