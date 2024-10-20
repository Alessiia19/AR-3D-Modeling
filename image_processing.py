from PIL import Image

def load_and_resize(image_path):
    img = Image.open(image_path)
    height = (480 if img.height > 480 else img.height) - (480 % 32)
    width = int(height * img.width / img.height)
    diff = width % 32
    width = width - diff if diff < 16 else width + 32 - diff
    img = img.resize((width, height))
    return img
