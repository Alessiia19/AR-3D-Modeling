import os
import matplotlib.pyplot as plt


# Visualizes an image and its corresponding depth map
def visualize_depth(img, depth_map):

    # Create a figure with two subplots for the image and depth map
    fig, ax = plt.subplots(1, 2)
    ax[0].imshow(img)
    ax[1].imshow(depth_map)

    # Remove axis ticks and labels for a cleaner visualization
    for a in ax:
        a.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

    plt.tight_layout()
    plt.show()


# Extracts the file name (without extension) from a given image path
def get_image_name(image_path):
    return os.path.splitext(os.path.basename(image_path))[0]