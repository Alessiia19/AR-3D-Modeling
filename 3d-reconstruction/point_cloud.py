import numpy as np
import open3d

# Creates a point cloud from an image and its corresponding depth map
def create_point_cloud(img, depth_map):
    w, h = img.size

    # Normalize and scale the depth map to an 8-bit format
    depth_img = (depth_map * 255 / np.max(depth_map)).astype('uint8')

    # Create an RGB-D image
    rgbd_img = open3d.geometry.RGBDImage.create_from_color_and_depth(
        open3d.geometry.Image(np.array(img)),    # Convert PIL image to Open3D format
        open3d.geometry.Image(depth_img),        # Depth image
        convert_rgb_to_intensity=False           # Preserve RGB information
    )

    # Set camera intrinsics
    camera_intrinsic = open3d.camera.PinholeCameraIntrinsic()
    camera_intrinsic.set_intrinsics(w, h, 500, 500, w / 2, h / 2)

    # Generate the point cloud from the RGB-D image and camera intrinsics
    pcd_raw = open3d.geometry.PointCloud.create_from_rgbd_image(rgbd_img, camera_intrinsic)

    return pcd_raw


# Processes a raw point cloud by removing outliers and estimating normals
def process_point_cloud(pcd_raw):

    # Remove statistical outliers to clean the point cloud
    pcd = pcd_raw.remove_statistical_outlier(nb_neighbors=20, std_ratio=6.0)[0]

    # Estimate normals for the point cloud
    pcd.estimate_normals()

    # Orient normals to align consistently in the same direction
    pcd.orient_normals_to_align_with_direction()
    
    return pcd
