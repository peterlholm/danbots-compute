"Stiching module"
from pathlib import Path
#from os.path import isfile, abspath
#from sys import stderr

import time

from utils.pcl_utils import pcl2jpg
from . import util
from . import registration as reg
from . import noise_removal as nr
# import meshing as mesh
# import evaluate as ev

O3D=False
if O3D:
    import open3d as o3d
    
_DEBUG = True
_SHOW = False
_TIMING = True

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
    components = [[o3d.io.read_point_cloud(str(Path(folder) / str(i) / filename)) for i in range(*cr)] for cr in component_ranges]
    print("length", len(components))
    print("length0", len(components[0]), type(components[0]))
    return components

def read_pointclouds(folder, filename='pointcloud.ply'):
    pcls = [o3d.io.read_point_cloud(str(Path(folder) / str(i) / filename)) for i in range(1, ANTAL+1)]
    return pcls

def read_pointcloud_tree(folder, filename='pointcloud.ply', maxnumber=100):
    "Read a standard tree of pointclouds. Returns pcl list"
    pcls = []
    i = 1
    OK = True
    while OK:
        file = Path(folder) / str(i) / filename
        if file.exists():
            pcls.append(o3d.io.read_point_cloud(str(file)))
        else:
            OK = False
        i += 1
        if i > maxnumber:
            OK = False
    return pcls

def read_model_pcl(folder, model):
    "Copy pcl to folder and read"
    folderfiles = sorted(Path(model).glob("*.ply"))
    pcls = []
    for file in folderfiles:
        pcls.append(o3d.io.read_point_cloud(str(file)))

    print (pcls)

def write_pointcloud(pcl, outfile):
    pcl2jpg(pcl, outfile)

def clean_point_cloud(pcd):
    # Pre-stitching cleaning parameters.
    epsilon = 0.35
    minimum_points = 7
    required_share = 0.06
    #print("input points", len(pcd.points) )
    pcd_result, kept_indicies = nr.keep_significant_clusters(pcd, required_share, epsilon, minimum_points)
    #print("Removing ", len(pcd.points) - len(kept_indicies), "points")
    return pcd_result

def reg_point_clouds(components):
    #print("Computing transformations component-wise using RANSAC and ICP.")
    components_with_transformations = [reg.get_transformations(components, voxel_size)]
    return components_with_transformations

def transform(components_with_transformations):
    #print("Applying transformations component-wise.")
    for component, transformations in components_with_transformations:
        util.transform(component, transformations)

def stitch_run(folder, maxnumber = 100):
    "stitching a folder tree"
    print("Stitching folder:", folder)
    # Start timer, parse config and run pipeline.
    overall_time_start = time.perf_counter()
    print("Loading data.")
    components = read_pointcloud_tree(folder, filename='pointcloud_filter.ply', maxnumber=maxnumber)
    if len(components) == 0:
        print("No pointclouds")
        return False
    stitch_pcl(components, folder)
    overall_timer_stop = time.perf_counter()
    print ("Time consumed", overall_timer_stop-overall_time_start)
    return True

def stitch_pcl(components, outfolder):
    time_start = time.perf_counter()
    pcls = []
    no_pointclouds = len(components)
    #no_pointclouds = 30
    print ("Number pointclouds:", no_pointclouds)
    if _DEBUG:
        print("cleaning pointclouds")
    for i in range(no_pointclouds):
        if _DEBUG:
            print("cleaning pointcloud", i)
        cpcl = clean_point_cloud(components[i])
        pcls.append(cpcl)
        if _DEBUG:
            write_pointcloud(components[i], outfolder / (f"in{(i+1):02}.jpg"))
            o3d.io.write_point_cloud(str(outfolder / (f"clean{(i+1):02}.ply")), cpcl)
            pcl2jpg(cpcl, outfolder / (f"clean{(i+1):02}.jpg"))
    if _TIMING:
        print("Cleaning finish", time.perf_counter()-time_start)
    # print(pcls)
    # print(len(pcls))

    if _DEBUG:
        print("Register pointclouds")
    comp_with_trans = reg_point_clouds(pcls)
    if _TIMING:
        print("Registering finish", time.perf_counter()-time_start)
    #print(registrations)

    if _DEBUG:
        print("Transform pointclouds")
    transform(comp_with_trans)
    if _DEBUG:
        print("Merging component-wise.")
    transformed_components, _ = zip(*comp_with_trans)
    merged_components = []
    print("merging")
    for component, name in zip(transformed_components, ["serie"]):
        print("start", name)
        merged = o3d.geometry.PointCloud()
        for pc in component:
            merged += pc
        merged_components.append(merged)
        if _SHOW:
            o3d.visualization.draw(merged, name)
        stitchfile = Path(outfolder) / 'stitch.ply'
        o3d.io.write_point_cloud(str(stitchfile), merged)

        pcl2jpg(merged, str(Path(outfolder) / 'stitch.jpg'))


