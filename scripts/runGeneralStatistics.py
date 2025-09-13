from pathlib import Path
import os
import json

_inferenceFilesPath = "inferenceResults/"

def get_datasets_from_inference_files():
    
    if not os.path.exists(_inferenceFilesPath):
        print("Error: Directory does not exist.")
    else:
        files = [f for f in os.listdir(_inferenceFilesPath) if os.path.isfile(os.path.join(_inferenceFilesPath, f))]
        return files


def select_datasets(datasets):

    print("Available datasets:\n")
    for i, dataset in enumerate(datasets):
        print(f"{i+1} - {str(dataset).split('_')[0]}")
    print("a - All")

    choice = input("\nChoose a dataset to extract metrics from (or q to quit): ")

    if choice.lower() == 'a':
        return datasets
    elif 1 <= int(choice) <= len(datasets):
        dataset = [datasets[int(choice) - 1]]
        return dataset
    else:
        print("Invalid choice")


def get_models_from_inference_files(selectedDataset):

    filePath = f"{_inferenceFilesPath}{selectedDataset}"
    with open(filePath) as f:
        data = json.load(f)
    
    models = list()

    for item in data['inference']:
        if item['model'] not in models:
            models.append(item['model'])

    if (len(models) > 0):
        return models
    else:
        print("No models available in the files given.")
        return false


def extract_model_statistics(selecteDataset, model):
    
    filePath = f"{_inferenceFilesPath}{selectedDataset}"
    
    truePositives = 0 
    falsePositives = 0
    falseNegatives = 0
    trueNegatives = 0

    errorOnPositiveOrMalignant = 0
    errorOnNegativeOrBenign = 0

    successfullCounter = 0
    failCounter = 0
    errorCounter = 0
    totalCounter = 0
    timeCounter = 0

    with open(filePath) as f:
        data = json.load(f)

    for item in data['inference']:
        if item['model'] == model:
            if ((item['name'].split('_')[-1].lower() == 'malignant') or (item['name'].split('_')[-1].lower() == 'positive')):
                isPositiveOrMalignant = True
            else:
                isPositiveOrMalignant = False
            if item['result'] == 'Successfull' and isPositiveOrMalignant:
                truePositives += 1
                successfullCounter += 1
            elif item['result'] == 'Successfull' and not isPositiveOrMalignant:
                trueNegatives += 1
                successfullCounter += 1
            elif item['result'] == 'Fail' and isPositiveOrMalignant:

            totalCounter += 1
            timeCounter += item['responseTime']



    return

if __name__ == "__main__":

    datasets = get_datasets_from_inference_files()
    selectedDatasets = select_datasets(datasets)

    for selectedDataset in selectedDatasets:
        models = get_models_from_inference_files(selectedDataset)
        for model in models:
            extract_model_statistics(selectedDataset, model)
            