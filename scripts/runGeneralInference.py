from pathlib import Path
import requests
import json
from PIL import Image
import os
import fileInteraction as fi
import ollamaInteraction as ollama
import parameters

def process_image(models, evalImage_path, dataset):

    print(f"\nProcessing model: {models}...\n")
    prompt = get_prompt_from_label(datasets)

    text = ollama.extract_knowledge_from_image(evalImage_path, models, prompt)
    print(f"\nResult: {text}\n\n")
    result = decide_result(models, evalImage_path, dataset)
    #add_file_entry(text, parameters.resultDirectory, models, dataset) #todo
    
    return

def decide_result(text, evalImagePath, dataset):
    
    loweredText = text.toLower()
    filenameWithoutExtension = os.path.basename(evalImagePath).rsplit('.', 1)[0]

    if dataset["type"] == "healthy/sick":

        if (("positive" in loweredText) and ("negative" in loweredText)):
            # manual mode
            return

        elif "positive" in loweredText:
            if "_sick" in filenameWithoutExtension:
                return "Successfull"
            elif "_healthy" in filenameWithoutExtension:
                return "Fail"
            else:
                raise ValueError("No appropriate appendix in filename")
                return "Error"

        elif "negative" in loweredText:
            if "_healthy" in filenameWithoutExtension:
                return "Successfull"
            elif "_sick" in filenameWithoutExtension:
                return "Fail"
            else:
                raise ValueError("No appropriate appendix in filename")
                return "Error"

        else: 
            return "Error"

    elif dataset["type"] == "benign/malignant":

        if (("malignant" in loweredText) and ("benign" in loweredText)):
            # manual mode
            return

        elif "malignant" in loweredText:
            if "_malignant" in filenameWithoutExtension:
                return "Successfull"
            elif "_benign" in filenameWithoutExtension:
                return "Fail"
            else:
                raise ValueError(f"No appropriate appendix in filename.{filenameWithoutExtension}")
                return "Error"

        elif "benign" in loweredText:
            if "_benign" in filenameWithoutExtension:
                return "Successfull"
            elif "_malignant" in filenameWithoutExtension:
                return "Fail"
            else:
                raise ValueError(f"No appropriate appendix in filename.{filenameWithoutExtension}")
                return "Error"

        else: 
            return "Error"

    else:
        raise ValueError(f"No appropriate dataset type.{dataset}")
        return "Error"

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
                return [parameters.directories[choice-1]]
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

    for dataset in datasets:
        for model in models:
            process_image(model, evalImage_path, parameters.resultDirectory, dataset) #do process directory, but prep datasets first
