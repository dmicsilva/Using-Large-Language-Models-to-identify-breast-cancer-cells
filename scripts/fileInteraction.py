import json
from PIL import Image
import base64
import os
import cv2

def encode_image_to_base64(image_path):
    
    if image_path.endswith(('.tif', '.tiff')):
        img = cv2.imread(image_path)
        return base64_string = base64.b64encode(cv2.imencode('.tiff', img)[1]).decode('utf-8') ##check
    else:
        return base64.b64encode(image_path.read_bytes()).decode('utf-8')

def save_to_json(filename, evalResult, output_dir, category, subcategory):

    metadata = {
        "fileName": filename,
        "evaluationResult": evalResult
    }

    output_path = os.path.join(output_dir, category, subcategory, f"{os.path.basename(os.path.splitext(image_path)[0])}.json")
    with open(output_path, 'w') as f:
        json.dump(metadata, f, indent=4)

def cycle_directory(directory):
    return