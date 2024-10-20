import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import open3d
from depth_estimation_model import DepthEstimationModel
from image_processing import load_and_resize
from depth_processing import normalize_and_rescale, post_process_depth
from point_cloud import create_point_cloud, process_point_cloud
from mesh import reconstruct_mesh, export_mesh
from utils import visualize_depth, get_image_name

def main(image_path):
    img = load_and_resize(image_path)
    
    model = DepthEstimationModel()
    predicted_depth = model.predict(img)

    depth_map_normalized = normalize_and_rescale(predicted_depth.squeeze().cpu().numpy())
    depth_map, cropped_img = post_process_depth(depth_map_normalized, img)
    #visualize_depth(cropped_img, depth_map)

    pcd_raw = create_point_cloud(cropped_img, depth_map)
    pcd = process_point_cloud(pcd_raw)
    
    mesh = reconstruct_mesh(pcd)
    open3d.visualization.draw_geometries([mesh], mesh_show_back_face=True)
   
    filename = get_image_name(image_path)
    export_mesh(mesh, filename)

if __name__ == "__main__":
    image_path = "C:\\Users\\aless\\Desktop\\DamaConErmellino.jpg" 
    main(image_path)
