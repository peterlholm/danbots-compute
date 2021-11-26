"Stiching module"
from pathlib import Path

from os.path import isfile, abspath
from sys import stderr
import open3d as o3d
import time

from utils.pcl_utils import pcl2jpg

from . import util
from . import registration as reg
from . import noise_removal as nr
# import meshing as mesh
# import evaluate as ev

ANTAL = 40
# Default values.
voxel_size = 0.3

# Mesh correction
low_density_threshold = 0.15

# Mesh detail
poisson_depth = 12

components = []

def xread_pointclouds(folder, filename='pointcloud.ply'):
    "return list of pointclouds"
    component_ranges = [[10, 20], [20, 30], [1, 10]]
    components = [[o3d.io.read_point_cloud(str(Path(folder) / str(i) / filename)) for i in range(*cr)]
                      for cr in component_ranges]
    print ("length",len(components))
    print ("length0", len(components[0]), type(components[0]))
    return components

def read_pointclouds(folder, filename='pointcloud.ply'):
    pcls = [o3d.io.read_point_cloud(str(Path(folder) / str(i) / filename)) for i in range(1,ANTAL+1)]
    return pcls

def write_pointcloud(pcl, outfile):
    pcl2jpg(pcl, outfile)

def clean_point_cloud(pcd):
    # Pre-stitching cleaning parameters.
    epsilon = 0.35
    minimum_points = 7
    required_share = 0.06
    print("input points", len(pcd.points) )
    pcd_result, kept_indicies = nr.keep_significant_clusters(pcd, required_share, epsilon, minimum_points)
    print("Removing ", len(pcd.points) - len(kept_indicies), "points")
    return pcd_result

def reg_point_clouds(components):
    print("Computing transformations component-wise using RANSAC and ICP.")
    components_with_transformations = [reg.get_transformations(components, voxel_size)]
    return components_with_transformations

def transform(components_with_transformations):
    print("Applying transformations component-wise.")
    for component, transformations in components_with_transformations:
        util.transform(component, transformations)

def stitch_run(folder):
    "stitching a folder tree"
    print("stitching folder:", folder)

    # Start timer, parse config and run pipeline.
    overall_time_start = time.perf_counter()
    print("Loading data.")
    components = read_pointclouds(folder)

    pcls = []
    for i in range(ANTAL):
        write_pointcloud(components[i], folder / ("in"+str(i)+".jpg"))
        cpcl = clean_point_cloud(components[i])
        o3d.io.write_point_cloud(str(folder / ("clean"+str(i)+".ply")), cpcl)
        pcls.append(cpcl)
        pcl2jpg(cpcl, folder / ("clean"+str(i)+".jpg"))

    #print(pcls)
    #print(len(pcls))
    comp_with_trans = reg_point_clouds(pcls)
    #print(registrations)

    transform(comp_with_trans)

    print("Merging component-wise.")
    transformed_components, _ = zip(*comp_with_trans)
    merged_components = []
    for component, name in zip(transformed_components, ["serie"]):
        merged = o3d.geometry.PointCloud()
        for pc in component:
            merged += pc
        merged_components.append(merged)
        if True:
            o3d.visualization.draw(merged, name)
        if True:
            o3d.io.write_point_cloud("{}.pcd".format(name), merged)