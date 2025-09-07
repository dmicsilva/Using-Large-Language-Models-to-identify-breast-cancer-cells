from pathlib import Path
import requests
import json
from PIL import Image
import os
import fileInteraction as fi
import ollamaInteraction as ollama
import parameters

def process_image(models, evalImage_path, dataset):

    print(f"\nProcessing model: {models}...")
    prompt = get_prompt_from_label(datasets)

    text = ollama.extract_knowledge_from_image(evalImage_path, models, prompt)
    print(text)
    add_file_entry(text, parameters.resultDirectory, models, dataset) #todo
    
    return


def choose_dataset():
    print("Select a dataset:")
    for i, directory in enumerate(parameters.directories):
        print(f"{i+1}. {directory['label']}")
    print("a - All")

    while True:
        choice = input("Enter the number of your chosen dataset (or 'q' to quit): ")
        
        if choice.lower() == "q":
            break
        elif choice.lower() == "a":
            parameters.directories

        try:
            choice = int(choice)
            if 1 <= choice <= len(directories):
                return parameters.directories[choice-1]
            else:
                print("Invalid choice. Please choose a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q' to quit.")


def get_prompt_from_label(dataset):
    
    for prompt in parameters.prompts:
        if prompt["label"] == dataset["label"]
            selectedPrompt = prompt["prompt"]
    
    if 'selectedPrompt' not in locals():
        raise ValueError(f"No matching label found: {dataset["label"]}")
    else
        return selectedPrompt


if __name__ == "__main__":

    datasets = choose_dataset()
    models = ollama.get_model()

    if isinstance(datasets, list):
        for dataset in datasets:
            if isinstance(models, list):
                for model in models:
                    process_image(model, evalImage_path, parameters.resultDirectory, dataset) #do process directory, but prep datasets first
            else:
                process_image(models, evalImage_path, parameters.resultDirectory, dataset)
    else:
        if isinstance(models, list):
            for model in models:
                process_image(model, evalImage_path, datasets)
        else:
            process_image(models, evalImage_path, datasets)
