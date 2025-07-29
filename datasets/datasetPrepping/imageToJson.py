import json
import base64
import os
from pathlib import Path

def encode_image_to_base64(image_path):
    """Convert an image file to base64 string."""
    return base64.b64encode(image_path.read_bytes()).decode('utf-8')

def save_to_json(base64_string, cancer_existance, output_dir):
    """
    Save the Base64 encoded string to a JSON file.

    Args:
        base64_string (str): A Base64 encoded string representing the image.
        cancer_existance (str): "Positive" or "Negative".

    Returns:
        None
    """

    # Create a dictionary to store the metadata
    metadata = {
        "base64_encoded_image": base64_string,
        "cancerExistance": cancer_existance
    }

    # Save the metadata to a JSON file
    output_path = os.path.join(output_dir, 'metadata.json')
    with open(output_path, 'w') as f:
        json.dump(metadata, f, indent=4)

# Example usage
image_path = Path(os.path.join(os.path.dirname(__file__),"parisTest.jpg"))
cancer_existance = "Positive"

base64_string = encode_image_to_base64(image_path)
save_to_json(base64_string, cancer_existance, os.path.dirname(__file__))