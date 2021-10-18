import numpy as np
from PIL import Image

_DEBUG=False

def nngenerate_pointcloud(rgb_file, mask_file,depth_file,ply_file):
    """
    Generate a colored point cloud in PLY format from a color and a depth image.
    
    Input:
    rgb_file -- filename of color image
    depth_file -- filename of depth image
    ply_file -- filename of ply file
    
    """
    rgb = Image.open(rgb_file)
    # depth = Image.open(depth_file)
    # depth = Image.open(depth_file).convert('I')
    depth = np.load(depth_file )
    mask = Image.open(mask_file).convert('I')

    # if rgb.size != depth.size:
    #     raise Exception("Color and depth image do not have  same resolution.")
    # if rgb.mode != "RGB":
    #     raise Exception("Color image is not in RGB format")
    # if depth.mode != "I":
    #     raise Exception("Depth image is not in intensity format")


    points = []    
    for v in range(rgb.size[1]):
        for u in range(rgb.size[0]):

            color =   rgb.getpixel((v,u))
            # Z = depth.getpixel((u,v)) / scalingFactor
            # if Z==0: continue
            # X = (u - centerX) * Z / focalLength
            # Y = (v - centerY) * Z / focalLength
            if (mask.getpixel((v,u))<55):
                # Z = depth.getpixel((u, v))
                Z = depth[u,v]
                if Z < 0:
                    Z = 0 
                else:
                    if Z> 80:
                        Z = 80
                if Z == 0: continue
                Y = .306 * (v-80) *  Z/80 #.306 = tan(FOV/2) = tan(34/2)
                X = .306 * (u-80) *  Z/80
                if (u==80 and v ==80) and _DEBUG:
                    print('80:z=', Z, X, Y)
                else:
                   if (u==102 and v ==82) and _DEBUG:
                        print('82:z=', Z, X, Y) 
                points.append("%f %f %f %d %d %d 0\n"%(X,Y,Z,color[0],color[1],color[2]))
    file = open(ply_file,"w")
    file.write('''ply
format ascii 1.0
element vertex %d
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
property uchar alpha
end_header
%s
'''%(len(points),"".join(points)))
    file.close()

