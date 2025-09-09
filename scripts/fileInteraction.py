import json
from PIL import Image
import base64
import os
import cv2
import parameters

def encode_image_to_base64(image_path):
    
    if image_path.endswith(('.tif', '.tiff')):
        img = cv2.imread(image_path)
        return base64.b64encode(cv2.imencode('.tif', img)[1]).decode('utf-8') ##check
    else:
        return base64.b64encode(image_path.read_bytes()).decode('utf-8')


def save_to_json(model, result, imageFilename, dataset, executionTime):

    filename = f"{dataset['label']}_inferences.json"
    
    if not os.path.exists(parameters.resultDirectory):
        os.makedirs(parameters.resultDirectory)
    
    filename = os.path.join(parameters.resultDirectory, filename)

    if not os.path.exists(filename):
        initial_data = {
            "totalInferences": 0,
            "totalTime": "0s",
            "filename": []
        }
        with open(filename, 'w') as f:
            json.dump(initial_data, f, indent=4)

    else:
        with open(filename, 'r') as f:
            data = json.load(f)

    data['filename'].append({
        "name": imageFilename,
        "model": model,
        "result": result,
        "responseTime": executionTime
    })

    data['totalInferences'] += 1
    data['totalTime'] = f"{float(data['totalTime'].split('s')[0]) + {executionTime}:.2f}s"

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

    return