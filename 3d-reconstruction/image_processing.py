from PIL import Image

# Loads an image from the given path and resizes it to a height and width that are both multiples of 32
def load_and_resize(image_path):
    # Load image
    img = Image.open(image_path)

    # Set the target height: capped at 480 or the original height if smaller, adjusted to be a multiple of 32
    height = (480 if img.height > 480 else img.height) - (480 % 32)

    # Maintain the aspect ratio while calculating the new width
    width = int(height * img.width / img.height)

    # Adjust the width to the nearest multiple of 32
    diff = width % 32
    width = width - diff if diff < 16 else width + 32 - diff

    # Resize the image
    img = img.resize((width, height))
    return img
