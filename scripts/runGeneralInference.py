from pathlib import Path
import requests
import json
from PIL import Image
import os
import time
import sys
import fileInteraction as fi
import ollamaInteraction as ollama
import parameters

def process_image(model, evalImage_path, dataset):

    filenameWithoutExtension = os.path.basename(evalImage_path).rsplit('.', 1)[0]

    print(f"\n\nProcessing image {filenameWithoutExtension} with model {model}...")
    prompt = get_prompt_from_label(datasets)

    startTime = time.time()
    text = ollama.extract_knowledge_from_image(evalImage_path, model, prompt)
    endTime = time.time()
    executionTime = endTime - startTime
    print("\033[1;33mResponse " + str(text) + "\033[0m")

    result = decide_result(text, filenameWithoutExtension, dataset)
    print(f"\nResult: {result}\n")

    fi.save_to_json(model, result, filenameWithoutExtension, dataset, executionTime)
    
    return

def decide_result(text, filenameWithoutExtension, dataset):
    
    loweredText = text.lower()

    if dataset['type'] == "healthy/sick":
        
        if (loweredText.endswith('positive') and len(text) > 200):
            if "_sick" in filenameWithoutExtension:
                return "Successfull"
            elif "_healthy" in filenameWithoutExtension:
                return "Fail"
            else:
                raise ValueError("No appropriate appendix in filename")
                return "Error"
        
        elif (loweredText.endswith('negative') and len(text) > 200):
            if "_sick" in filenameWithoutExtension:
                return "Fail"
            elif "_healthy" in filenameWithoutExtension:
                return "Successfull"
            else:
                raise ValueError("No appropriate appendix in filename")
                return "Error"

        if ("can't help" in loweredText or "provide" in loweredText) and not (("positive" in loweredText) or ("negative" in loweredText)):
            return "Error"

        if ((("positive" in loweredText) and ("negative" in loweredText)) or len(text) > 200):
            return manual_review_mode(filenameWithoutExtension, text)

        elif "positive" in loweredText:
            if "_sick" in filenameWithoutExtension:
                return "Successfull"
            elif "_healthy" in filenameWithoutExtension:
                return "Fail"
            else:
                raise ValueError("No appropriate appendix in filename")
                return "Error"

        elif "negative" in loweredText or "no signs of" in loweredText:
            if "_healthy" in filenameWithoutExtension:
                return "Successfull"
            elif "_sick" in filenameWithoutExtension:
                return "Fail"
            else:
                raise ValueError("No appropriate appendix in filename")
                return "Error"

        else: 
            return "Error"

    elif dataset['type'] == "benign/malignant":

        if (loweredText.endswith('malignant') and len(text) > 200):
            if "_malignant" in filenameWithoutExtension:
                return "Successfull"
            elif "_benign" in filenameWithoutExtension:
                return "Fail"
            else:
                raise ValueError("No appropriate appendix in filename")
                return "Error"
        
        elif (loweredText.endswith('benign') and len(text) > 200):
            if "_malignant" in filenameWithoutExtension:
                return "Fail"
            elif "_benign" in filenameWithoutExtension:
                return "Successfull"
            else:
                raise ValueError("No appropriate appendix in filename")
                return "Error"

        if ("can't help" in loweredText or "provide" in loweredText) and not (("malignant" in loweredText) or ("benign" in loweredText)):
            return "Error"

        if ((("malignant" in loweredText) and ("benign" in loweredText)) or len(text) > 200):
            return manual_review_mode(filenameWithoutExtension, text)

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


def manual_review_mode(filenameWithoutExtension, text):

    print("\n\033[1;91mManual Review Mode\033[0m\n")
    os.system('echo -e "\a"')

    while True:
        choice = input("Enter S - Successfull; F - Fail; E - Error: ")

        if choice.lower() == 's':
            return "Successfull"
        elif choice.lower() == 'f':
            return "Fail"
        elif choice.lower() == 'e':
            return "Error"
        else:
            print("Invalid choice. Please choose a valid number.\n")

                    
def choose_dataset():
    print("Select a dataset:")
    for i, directory in enumerate(parameters.directories):
        print(f"{i+1}. {directory['label']}")
    print("a - All")

    while True:
        choice = input("Enter the number of your chosen dataset (or 'q' to quit): ")
        
        if choice.lower() == "q":
            sys.exit()
        elif choice.lower() == "a":
            parameters.directories

        try:
            choice = int(choice)
            if 1 <= choice <= len(parameters.directories):
                return [parameters.directories[choice-1]]
            else:
                print("Invalid choice. Please choose a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q' to quit.")


def get_prompt_from_label(dataset):
    
    for prompt in parameters.prompts:
        if prompt['label'] == dataset[0]['label']:
            selectedPrompt = prompt['prompt']
    
    if 'selectedPrompt' not in locals():
        raise ValueError(f"No matching label found: {dataset['label']}")
    else:
        return selectedPrompt


if __name__ == "__main__":

    datasets = choose_dataset()
    models = ollama.get_model()

    for dataset in datasets:
        for model in models:
            for dirpath, dirnames, filenames in os.walk(dataset['path']):
                for filename in filenames:
                    if filename.endswith(('.jpg', '.png', '.tif')):
                        if (not fi.check_entry_existance(dataset, model, filename.split('.')[0])):    
                            imagePath = Path(os.path.join(dirpath, filename))
                            process_image(model, imagePath, dataset)
                        else:
                            print(f"\nImage already analyzed for this dataset ({dataset['label']}) -> {filename}\n")
                        