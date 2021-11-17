"pointcload utils"
import open3d as o3d
import numpy as np
from matplotlib import pyplot as plt

OBJ_CENTER = [0.0,0.0,22.0]
CAM_POSITION = [-10.0, -0.0, -25.0]
ZOOM = 0.3

_DEBUG = False

def mirror_pcl(infile, outfile):
    "Mirror pcl about X axis"
    pcd = o3d.io.read_point_cloud(str(infile))
    arr = np.asarray(pcd.points)
    #print('xyz_load', arr)
    for pkt in arr:
        pkt[0] = -pkt[0]
    #print('xyz_load', arr)
    opcd = o3d.geometry.PointCloud()
    opcd.points = o3d.utility.Vector3dVector(arr)
    o3d.io.write_point_cloud(str(outfile), opcd)

def pcl2jpg(pcd, outfile):
    vis = o3d.visualization.Visualizer()
    res = vis.create_window(visible = _DEBUG, width=500, height=500)
    if not res:
        print("create window result", res)
    vis.add_geometry(pcd)
    #is.get_render_option().load_from_json("Imaging/di
    # splay/RenderOption.json")
    ctr = vis.get_view_control()
    if ctr is None:
        print("pcl2jpg cant get view_control", vis)
    ctr.set_zoom(ZOOM)
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
    axe = plt.axes(projection='3d')
    axe.scatter(arr[:,0], arr[:,1], arr[:,2], c = "#222222", s=0.1)
    plt.savefig(outfile)
    #plt.show()

def ply2jpg(infile, outfile):
    #print(infile)
    #print(outfile)
    pcd = o3d.io.read_point_cloud(str(infile))
    pcl2jpg(pcd, outfile)
    #render_image(pcd, outfile)

#ply2jpg(Path(__file__+'/../../testdata/render0/pointcl-nndepth.ply'), 'ud.jpg')

# maybe not used
def pcl2png(infilename, outfilename):
    "write file with pointcloud"
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

def mask_pcl(pcl_filename, mask_filename, out_filename):
    "mask pointcloud from maskfile"
    print("Masking pcl", pcl_filename, mask_filename, out_filename)
    pcd = o3d.io.read_point_cloud(str(pcl_filename))
    arr = np.asarray(pcd.points)
    _mask = np.load(mask_filename)

    #print('xyz_load', arr)
    for pkt in arr:
        print(pkt)
        #pkt[0] = -pkt[0]
    #print('xyz_load', arr)
    opcd = o3d.geometry.PointCloud()
    opcd.points = o3d.utility.Vector3dVector(arr)
    o3d.io.write_point_cloud(str(out_filename), opcd)
