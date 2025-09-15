from pathlib import Path
import os
import json
import fileInteraction as fi

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


def extract_model_statistics(selectedDataset, model):
    
    filePath = f"{_inferenceFilesPath}{selectedDataset}"

    if os.path.exists(_inferenceFilesPath):
        with open(filePath) as f:
            data = json.load(f)
        
        ignoreModel = False
        for item in data:
            if item['model'] == model:
                ignoreModel = True
        
        if ignoreModel:
            print(f"Statistics already extracted for {model} from dataset {selectedDataset}")
            return

    else:
        with open(filePath) as f:
            data = json.load(f)
    
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
                falsePositives += 1
                failCounter +=1
            elif item['result'] == 'Fail' and not isPositiveOrMalignant:
                falseNegatives += 1
                failCounter += 1
            elif item['result'] == 'Error' and isPositiveOrMalignant:
                errorOnPositiveOrMalignant += 1
                errorCounter += 1
            elif item['result'] == 'Error' and not isPositiveOrMalignant:
                errorOnNegativeOrBenign += 1
                errorCounter += 1
            else:
                print(f"Case not handled -> {item['name']} on dataset {selectedDataset} on model {model}")

            totalCounter += 1
            timeCounter += item['responseTime']
    
    precision = truePositives / (truePositives + falsePositives + errorOnPositiveOrMalignant) if (truePositives + falsePositives + errorOnPositiveOrMalignant) > 0 else 0
    specificity = trueNegatives / (trueNegatives + falsePositives + errorOnPositiveOrMalignant) if (trueNegatives + falsePositives + errorOnPositiveOrMalignant) > 0 else 0
    recall = truePositives / (truePositives + falseNegatives + errorOnNegativeOrBenign) if (truePositives + falseNegatives + errorOnNegativeOrBenign) > 0 else 0
    f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    accuracy = (truePositives + trueNegatives) / totalCounter

    successRate = successfullCounter / totalCounter
    failRate = failCounter / totalCounter
    errorRate = errorCounter / totalCounter
    errorOnPositiveOrMalignantRate = errorOnPositiveOrMalignant / totalCounter
    errorOnNegativeOrBenignRate = errorOnNegativeOrBenign / totalCounter

    falsePositiveRate = falsePositives / (falsePositives + trueNegatives + errorOnPositiveOrMalignant) if (falsePositives + trueNegatives + errorOnPositiveOrMalignant) > 0 else 0
    falseNegativeRate = falseNegatives / (falseNegatives + truePositives + errorOnNegativeOrBenign) if (falseNegatives + truePositives + errorOnNegativeOrBenign) > 0 else 0

    print(f"{selectedDataset} Inference Statistics on model {model}\n")
    print(f"Precision: {precision:.4f}\nSpecificity: {specificity:.4f}\nRecall: {recall:.4f}\nF1 Score: {f1_score:.4f}\nAccuracy: {accuracy:.4f}\n")
    print(f"Success Rate: {successRate:.4f}\nFail Rate: {failRate:.4f}\nError Rate: {errorRate:.4f}\n")
    print(f"Error on positive/malignant Rate: {errorOnPositiveOrMalignantRate:.4f}\nError on negative/benign Rate: {errorOnNegativeOrBenignRate:.4f}\n")
    print(f"False positive Rate: {falsePositiveRate:.4f}\nFalseNegativeRate: {falseNegativeRate:.4f}\n")
    print(f"{timeCounter:.2f}s")

    data = {
        "model": model,
        "totalInferences": totalCounter,
        "totalTime": f"{timeCounter:.2f}s",
        "statistics": [
            {"mainMetrics": [],
            "mainRates": [],
            "otherRates": []}
        ]
    }

    data["statistics"][0]["mainMetrics"].append({
        "precision": precision,
        "specificity": specificity,
        "recall": recall,
        "f1_score": f1_score,
        "accuracy": accuracy,
    })

    data["statistics"][0]["mainRates"].append({
        "success_rate": successRate,
        "fail_rate": failRate,
        "error_rate": errorRate,
    })

    data["statistics"][0]["otherRates"].append({
        "error_on_positive_or_malignant_rate": errorOnPositiveOrMalignantRate,
        "error_on_negative_or_benign_rate": errorOnNegativeOrBenignRate,
        "false_positive_rate": falsePositiveRate,
        "false_negative_rate": falseNegativeRate
    })

    fi.save_statistics_to_json(selectedDataset, data)

    return

if __name__ == "__main__":

    datasets = get_datasets_from_inference_files()
    selectedDatasets = select_datasets(datasets)

    for selectedDataset in selectedDatasets:
        models = get_models_from_inference_files(selectedDataset)
        for model in models:
            extract_model_statistics(selectedDataset, model)
            