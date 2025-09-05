from pathlib import Path
import requests
import json
from PIL import Image
import os
import fileInteraction as fi
import ollamaInteraction as ollama

endpoint = "http://localhost:11434/api/chat"
directories = [
    {"label": "MRI", "path": "/home/buybluepants/Documents/Using-Large-Language-Models-to-identify-breast-cancer-cells/datasets/Breast Cancer Patients MRI's"},
]

def process_image(models, evalImage_path, resultDirectory):

    print(f"\nProcessing model: {models}...")

    text = extract_knowledge_from_image(evalImage_path, models)
    print(text)
    add_file_entry(text, resultFile_path, models) #todo
    
    return

def choose_dataset():
    print("Select a directory:")
    for i, directory in enumerate(directories):
        print(f"{i+1}. {directory['label']}")

    while True:
        choice = input("Enter the number of your chosen directory (or 'q' to quit): ")
        
        if choice.lower() == "q":
            break

        try:
            choice = int(choice)
            if 1 <= choice <= len(directories):
                selected_directory = directories[choice-1]
                return selected_directory['path']
            else:
                print("Invalid choice. Please choose a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q' to quit.")

def cycle_directory(directory):
    return

if __name__ == "__main__":

    evalDirectory = choose_dataset()
    evalImage_path = Path('/home/buybluepants/Documents/Thesis/Using-Large-Language-Models-to-identify-breast-cancer-cells/datasets/Breast Cancer Patients MRI\'s/validation/Healthy/S_75.jpg')
    resultDirectory = Path('/home/buybluepants/Documents/Using-Large-Language-Models-to-identify-breast-cancer-cells/results')

    models = ollama.get_model()
    process_image(models, evalImage_path, resultDirectory)