"convert from pointcloud to jpg picture"
#from pathlib import Path
import numpy as np
import open3d as o3d
from matplotlib import pyplot as plt

OBJ_CENTER = [0.0,0.0,22.0]
CAM_POSITION = [-10.0, -0.0, -25.0]

_DEBUG = False

def pcl2jpg(pcd, outfile):
    vis = o3d.visualization.Visualizer()
    vis.create_window(visible = _DEBUG, width=500, height=500)
    vis.add_geometry(pcd)
    #is.get_render_option().load_from_json("Imaging/di
    # splay/RenderOption.json")
    ctr = vis.get_view_control()
    ctr.set_zoom(0.4)
    ctr.set_front(CAM_POSITION)
    ctr.set_lookat(OBJ_CENTER)
    ctr.set_up([+10.0, 0, 0])
    opt = vis.get_render_option()
    opt.point_size = 1.0
    #opt.point_color_option.Color = 1
    #vis.run()
    if _DEBUG:
        img = vis.capture_screen_float_buffer(True)
        plt.imshow(np.asarray(img))
    vis.capture_screen_image(str(outfile), do_render=True)

def render_image(pcd, outfile):
    arr = np.asarray(pcd.points)
    #print(arr)
    ax = plt.axes(projection='3d')
    ax.scatter(arr[:,0], arr[:,1], arr[:,2], c = "#222222", s=0.1)
    plt.savefig(outfile)
    #plt.show()

def ply2jpg(infile, outfile):
    #print(infile)
    #print(outfile)
    pcd = o3d.io.read_point_cloud(str(infile))
    pcl2jpg(pcd, outfile)
    #render_image(pcd, outfile)

#ply2jpg(Path(__file__+'/../../testdata/render0/pointcl-nndepth.ply'), 'ud.jpg')
