import numpy as np
import torch
from PIL import Image

# Normalizes and rescales the depth map to a specified range
def normalize_and_rescale(depth_map, new_min_val=1, new_max_val=0.6):

    # Find the minimum and maximum values in the depth map
    min_val = np.min(depth_map)
    max_val = np.max(depth_map)

    # Normalize the depth map
    depth_normalized = (depth_map - min_val) / (max_val - min_val)
    
    # Rescale the normalized depth map to the new range 
    depth_rescaled = depth_normalized * (new_max_val - new_min_val) + new_min_val
    return depth_rescaled 


'''
Post-processes the depth map by cropping the borders and resizing to match the input image dimensions
Parameters:
        predicted_depth (numpy.ndarray): The predicted depth map to be post-processed
        img (PIL.Image): The input image corresponding to the depth map
        pad (int): The number of pixels to crop from each side of the depth map
'''
def post_process_depth(predicted_depth, img, pad=8):

    # Crop the depth map to remove border artifacts.
    # Scale the depth values by 1000 for better representation
    output = (predicted_depth * 1000.0)[pad:-pad, pad:-pad]

    # Crop and resize the input image and depth map to ensure matching dimensions
    img = img.crop((pad, pad, img.width - pad, img.height - pad))
    output_resized = Image.fromarray(output).resize((img.width, img.height))

    return np.array(output_resized), img
