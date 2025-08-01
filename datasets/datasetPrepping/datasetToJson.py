import json
from PIL import Image
import base64
import os

def image_to_base64(image_path):
    """
    Convert an image into a Base64 encoded string.

    Args:
        image_path (str): Path to the input image.

    Returns:
        str: A Base64 encoded string representing the image.
    """

    # Open the image using Pillow
    with Image.open(image_path) as img:
        # Convert the image to bytes
        img_bytes = img.tobytes()

        # Encode the bytes into a Base64 string
        base64_string = base64.b64encode(img_bytes).decode('utf-8')

    return base64_string

def save_to_json(base64_string, cancer_existance, output_dir, category, subcategory):
    """
    Save the Base64 encoded string to a JSON file.

    Args:
        base64_string (str): A Base64 encoded string representing the image.
        cancer_existance (str): "Positive" or "Negative".
        output_dir (str): Directory where the JSON file will be saved.

    Returns:
        None
    """

    # Create a dictionary to store the metadata
    metadata = {
        "base64_encoded_image": base64_string,
        "cancerExistance": cancer_existance
    }

    # Save the metadata to a JSON file
    output_path = os.path.join(output_dir, category, subcategory, f"{os.path.basename(os.path.splitext(image_path)[0])}.json")
    with open(output_path, 'w') as f:
        json.dump(metadata, f, indent=4)

# Specify the directories
input_dir = '/home/buybluepants/Documents/Using-Large-Language-Models-to-identify-breast-cancer-cells/datasets/Breast Cancer Patients MRI\'s'

# Create output directories recursively

output_subdirs = [os.path.join(f"JSON_{os.path.basename(input_dir)}", "train", "Healthy"), os.path.join(f"JSON_{os.path.basename(input_dir)}", "train", "Sick"), os.path.join(f"JSON_{os.path.basename(input_dir)}", "validation", "Healthy"), os.path.join(f"JSON_{os.path.basename(input_dir)}", "validation", "Sick")]
for subdir in output_subdirs:
    try:
        os.makedirs(subdir)
    except FileExistsError:
        pass

# Cycle through all the subdirectories and their images
for category in os.listdir(input_dir):
    for subcategory in os.listdir(os.path.join(input_dir, category)):
        if subcategory == "Healthy":
            cancer_existance = "Negative"
        elif subcategory == "Sick":
            cancer_existance = "Positive"

        for file in os.listdir(os.path.join(input_dir, category, subcategory)):
            image_path = os.path.join(input_dir, category, subcategory, file)
            base64_string = image_to_base64(image_path)
            save_to_json(base64_string, cancer_existance, os.path.join(f"JSON_{os.path.basename(input_dir)}"), category, subcategory)