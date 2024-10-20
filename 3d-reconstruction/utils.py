import os
import matplotlib.pyplot as plt

def visualize_depth(img, depth_map):
    fig, ax = plt.subplots(1, 2)
    ax[0].imshow(img)
    ax[1].imshow(depth_map)
    for a in ax:
        a.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
    plt.tight_layout()
    plt.show()

def get_image_name(image_path):
    return os.path.splitext(os.path.basename(image_path))[0]