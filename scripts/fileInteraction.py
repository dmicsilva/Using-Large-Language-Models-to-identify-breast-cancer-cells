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

def deep_merge(a: dict, b: dict) -> dict:
    for k, v in b.items():
        if (
            k in a
            and isinstance(a[k], dict)
            and isinstance(v, dict)
        ):
            deep_merge(a[k], v)
        else:
            a[k] = v
    return a

def add_or_append(dest: dict, new: dict, *, list_key: str | None = None) -> dict:
    """
    * Add every key/value from `new` into `dest`.
    * If a key already exists:
        - If it maps to a list and `list_key` is that key,
          append the new value to the list.
        - Otherwise, **do nothing** – we preserve the old value.
    """
    for k, v in new.items():
        if k in dest:
            # Special case: we want to append to a list
            if list_key and k == list_key and isinstance(dest[k], list):
                dest[k].append(v)
            else:
                # Key exists → keep the old value
                pass
        else:
            dest[k] = v
    return dest

def save_statistics_to_json(selectedDataset, data):
    
    filename = f"{selectedDataset.split('_')[0]}_statistics.json"

    if not os.path.exists(parameters.statisticsDirectory):
        os.makedirs(parameters.statisticsDirectory)
    
    filename = os.path.join(parameters.statisticsDirectory, filename)

    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump([data], f, indent=4)
        return
    
    else:
        with open(filename, 'r') as f:
            existingData = json.load(f)
        existingData.append(data)
        with open(filename, 'w') as file:
            json.dump(existingData, file, indent=4)

    return

        
    