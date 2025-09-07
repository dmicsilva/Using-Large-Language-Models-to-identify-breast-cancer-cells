import json
from PIL import Image
import base64
import os

def encode_image_to_base64(image_path):
    """Convert an image file to base64 string."""
    return base64.b64encode(image_path.read_bytes()).decode('utf-8')

def save_to_json(filename, evalResult, output_dir, category, subcategory):

    # Create a dictionary to store the metadata
    metadata = {
        "fileName": filename,
        "evaluationResult": evalResult
    }

    # Save the metadata to a JSON file
    output_path = os.path.join(output_dir, category, subcategory, f"{os.path.basename(os.path.splitext(image_path)[0])}.json")
    with open(output_path, 'w') as f:
        json.dump(metadata, f, indent=4)

def cycle_directory(directory):
    return