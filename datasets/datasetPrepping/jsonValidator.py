import os
import json
from pathlib import Path

_isBad = False

def validate_json_files(directory):
    """
    Iterates through a directory and its subdirectories, and validates the JSON files found.
    
    Args:
        directory (str): The path to the directory to be scanned.
    """
    try:
        with open(directory, 'r') as f:
            json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error in JSON file '{file_path}': {e}")
        _isBad = True

if __name__ == "__main__":

    cwd = os.getcwd()
    src_folder = os.path.join(cwd, 'datasets/datasetPrepping/Json_mammogramDataset')
    subfolders_to_process = ['healthy', 'sick']

    for subfolder in subfolders_to_process:
        src_path = os.path.join(src_folder, subfolder)
        for filename in os.listdir(src_path):
            imagePath = Path(os.path.join(src_path, filename))
            validate_json_files(imagePath)

    if _isBad:
        print("Dataset not valid")
    else:
        print("Valid Dataset")