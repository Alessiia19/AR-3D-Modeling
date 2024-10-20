import numpy as np
import torch
from PIL import Image

def normalize_and_rescale(depth_map, new_min_val=1, new_max_val=0.7):
    min_val = np.min(depth_map)
    max_val = np.max(depth_map)
    depth_normalized = (depth_map - min_val) / (max_val - min_val)
    
    depth_rescaled = depth_normalized * (new_max_val - new_min_val) + new_min_val
    res = torch.tensor(depth_rescaled).unsqueeze(0).unsqueeze(0)
    return res 

def post_process_depth(predicted_depth, img, pad=8):
    output = (predicted_depth.squeeze().cpu().numpy() * 1000.0)[pad:-pad, pad:-pad]
    img = img.crop((pad, pad, img.width - pad, img.height - pad))

    output_resized = Image.fromarray(output).resize((img.width, img.height))
    return np.array(output_resized), img
