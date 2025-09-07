from pathlib import Path
import requests
import json
from PIL import Image
import os
import fileInteraction as fi
import ollamaInteraction as ollama

_endpoint = "http://localhost:11434/api/chat"
_directories = [
    {"label": "MRI", "path": "/home/buybluepants/Documents/Using-Large-Language-Models-to-identify-breast-cancer-cells/datasets/Breast Cancer Patients MRI's"},
    {"label": "Mammogram", "path": "/home/buybluepants/Documents/Using-Large-Language-Models-to-identify-breast-cancer-cells/datasets/breast-cancer-detection-mammogram"},
    {"label": "Ultrasound", "path": "/home/buybluepants/Documents/Using-Large-Language-Models-to-identify-breast-cancer-cells/datasets/BrEaST-Lesions_USG-images_and_masks"},
    {"label": "Thermography", "path": "/home/buybluepants/Documents/Using-Large-Language-Models-to-identify-breast-cancer-cells/datasets/BCD_Dataset-thermogram"},
    {"label": "Histopathology", "path": "/home/buybluepants/Documents/Using-Large-Language-Models-to-identify-breast-cancer-cells/datasets/Breast Cancer Patients MRI's"},
]
_resultDirectory = Path('/home/buybluepants/Documents/Using-Large-Language-Models-to-identify-breast-cancer-cells/results')

def process_image(models, evalImage_path, _resultDirectory):

    print(f"\nProcessing model: {models}...")

    text = extract_knowledge_from_image(evalImage_path, models, _endpoint)
    print(text)
    add_file_entry(text, resultFile_path, models) #todo
    
    return

def choose_dataset():
    print("Select a dataset:")
    for i, directory in enumerate(_directories):
        print(f"{i+1}. {_directory['label']}")

    while True:
        choice = input("Enter the number of your chosen dataset (or 'q' to quit): ")
        
        if choice.lower() == "q":
            break

        try:
            choice = int(choice)
            if 1 <= choice <= len(directories):
                return _directories[choice-1]
            else:
                print("Invalid choice. Please choose a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q' to quit.")


if __name__ == "__main__":

    evalDirectory = choose_dataset()
    models = ollama.get_model()
    process_image(models, evalImage_path, _resultDirectory)