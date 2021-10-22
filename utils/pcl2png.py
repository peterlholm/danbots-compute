"""
Create png file from .ply pointcloud
"""

#from pathlib import Path
import numpy as np
import open3d as o3d
from matplotlib import pyplot as plt

def pcl2png(infilename, outfilename):
    pcd = o3d.io.read_point_cloud(str(infilename))
    vis = o3d.visualization.Visualizer()
    vis.create_window(visible = False)
    vis.add_geometry(pcd)
    #is.get_render_option().load_from_json("Imaging/display/RenderOption.json")
    ctr = vis.get_view_control()
    ctr.set_zoom(0.45)
    ctr.set_front([-0.084777469999256949, -0.30273583588141922, -0.94929647331784794])
    ctr.set_lookat([0.0,0.0,26.0])
    ctr.set_up([+10.20694, 0, 00])
    #vis.run()
    img = vis.capture_screen_float_buffer(True)
    plt.imshow(np.asarray(img))
    vis.capture_screen_image(str(outfilename), do_render=True)
