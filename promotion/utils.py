import os
from PIL import Image
from django.conf import settings

# Define the folder where images are stored
PROMOTION_DIR = os.path.join(settings.BASE_DIR, 'static/promotion/')

def save_promotion_image(image, image_name):    
    # Checking Directory
    if not os.path.exists(PROMOTION_DIR):
        os.makedirs(PROMOTION_DIR)  

    # Convert filename to PNG
    filename = f"{image_name}.png"
    file_path = os.path.join(PROMOTION_DIR, filename)

    # Convert and save the image as PNG
    img = Image.open(image)
    img.save(file_path, "PNG")

    return filename  # Returning just the image name
