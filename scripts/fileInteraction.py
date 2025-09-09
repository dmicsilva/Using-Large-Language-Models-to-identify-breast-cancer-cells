import json
from PIL import Image
import base64
import os
import cv2
import parameters

def encode_image_to_base64(image_path):
    
    if str(image_path).endswith(('.tif', '.tiff')):
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
        data = {
            "totalInferences": 0,
            "totalTime": "0s",
            "inference": []
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    else:
        with open(filename, 'r') as f:
            data = json.load(f)

    data['inference'].append({
        "name": imageFilename,
        "model": model,
        "result": result,
        "responseTime": executionTime
    })

    data['totalInferences'] += 1

    initialTime = float(data['totalTime'].split('s')[0])
    incrementedTime = initialTime + executionTime
    data['totalTime'] = f"{incrementedTime:.2f}s"

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

    return