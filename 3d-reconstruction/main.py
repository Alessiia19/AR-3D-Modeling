import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import open3d
from depth_estimation_model import DepthEstimationModel
from image_processing import load_and_resize
from depth_processing import normalize_and_rescale, post_process_depth
from point_cloud import create_point_cloud, process_point_cloud
from mesh import reconstruct_mesh, export_mesh
from utils import visualize_depth, get_image_name


'''
Main function to generate a 3D model from a given input image
Parameters:
    image_path(str): path to the input image file
'''
def main(image_path):

    # Load and resize the input image
    img = load_and_resize(image_path)
    
    # Depth estimation models initialization 
    model = DepthEstimationModel()
    predicted_depth = model.predict(img)

    # Depth map post-processing and visualization
    depth_map_normalized = normalize_and_rescale(predicted_depth.squeeze().cpu().numpy())
    depth_map, cropped_img = post_process_depth(depth_map_normalized, img)
    visualize_depth(cropped_img, depth_map)

    # Generate the point cloud
    pcd_raw = create_point_cloud(cropped_img, depth_map)

    # Point cloud post-processing and visualization
    pcd = process_point_cloud(pcd_raw)
    open3d.visualization.draw_geometries([pcd])

    # Mesh reconstruction and visualization
    mesh = reconstruct_mesh(pcd)
    open3d.visualization.draw_geometries([mesh], mesh_show_back_face=True)
   
   # Export mesh
    filename = get_image_name(image_path)
    export_mesh(mesh, filename)

