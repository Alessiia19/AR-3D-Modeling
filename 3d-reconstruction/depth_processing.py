import numpy as np
import torch
from PIL import Image

def normalize_and_rescale(depth_map, new_min_val=1, new_max_val=0.6):
    min_val = np.min(depth_map)
    max_val = np.max(depth_map)
    depth_normalized = (depth_map - min_val) / (max_val - min_val)
    
    depth_rescaled = depth_normalized * (new_max_val - new_min_val) + new_min_val
    return depth_rescaled 

def post_process_depth(predicted_depth, img, pad=8):
    output = (predicted_depth * 1000.0)[pad:-pad, pad:-pad]
    img = img.crop((pad, pad, img.width - pad, img.height - pad))

    output_resized = Image.fromarray(output).resize((img.width, img.height))
    return np.array(output_resized), img
