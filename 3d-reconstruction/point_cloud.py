import numpy as np
import open3d

def create_point_cloud(img, depth_map):
    w, h = img.size
    depth_img = (depth_map * 255 / np.max(depth_map)).astype('uint8')
    rgbd_img = open3d.geometry.RGBDImage.create_from_color_and_depth(
        open3d.geometry.Image(np.array(img)),
        open3d.geometry.Image(depth_img),
        convert_rgb_to_intensity=False
    )
    camera_intrinsic = open3d.camera.PinholeCameraIntrinsic()
    camera_intrinsic.set_intrinsics(w, h, 500, 500, w / 2, h / 2)

    pcd_raw = open3d.geometry.PointCloud.create_from_rgbd_image(rgbd_img, camera_intrinsic)
    return pcd_raw

def process_point_cloud(pcd_raw):
    pcd = pcd_raw.remove_statistical_outlier(nb_neighbors=20, std_ratio=6.0)[0]
    pcd.estimate_normals()
    pcd.orient_normals_to_align_with_direction()
    return pcd
