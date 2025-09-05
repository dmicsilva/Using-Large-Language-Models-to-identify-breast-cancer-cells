import json
from PIL import Image
import base64
import os

def encode_image_to_base64(image_path):
    """Convert an image file to base64 string."""
    return base64.b64encode(image_path.read_bytes()).decode('utf-8')

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
