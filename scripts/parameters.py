from pathlib import Path
import os

cwd = os.getcwd()

endpoint = "http://localhost:11434/api/chat"
getModelEndpoint = "http://localhost:11434/api/tags"

directories = [
    {"label": "MRI", "path": os.path.join(cwd, 'datasets/datasetPrepping/mriDataset'), "type": "healthy/sick"},
    {"label": "Mammogram", "path": os.path.join(cwd, 'datasets/datasetPrepping/mammogramDataset'), "type": "healthy/sick"},
    {"label": "Ultrasound", "path": os.path.join(cwd, 'datasets/datasetPrepping/ultrasoundDataset'), "type": "benign/malignant"},
    {"label": "UltrasoundMasks", "path": os.path.join(cwd, 'datasets/datasetPrepping/ultrasoundMasksDataset'), "type": "benign/malignant"},
    {"label": "Thermography", "path": os.path.join(cwd, 'datasets/datasetPrepping/thermogramDataset'), "type": "healthy/sick"},
    {"label": "Histopathology", "path": os.path.join(cwd, 'datasets/datasetPrepping/histopathologyDataset'), "type": "benign/malignant"},
    {"label": "HistopathologyMasks", "path": os.path.join(cwd, 'datasets/datasetPrepping/histopathologyMasksDataset'), "type": "benign/malignant"},
]

resultDirectory = os.path.join(cwd, 'inferenceResults')
statisticsDirectory = os.path.join(cwd, 'inferenceStatistics')

prompts = [
    {"label": "MRI", "prompt": "You are a model that evaluates the existance of breast cancer from an image of a MRI exam. \n"
                    "Respond with only 'positive' or 'negative' according to the result of the analysis of your evaluation of the given image. Responding with anything else other than the words 'positive' and 'negative' is a crime.\n"
                    "Don't look for a diagnosis or treatment plan, just make the evaluation. \n"
                    "Don't use paragraphs or newline. Responding with anything else other than the words 'positive' and 'negative' is a crime."},
    {"label": "Mammogram", "prompt": "You are a model that evaluates the existance of breast cancer from an image of a mammogram exam. \n"
                    "Respond with only 'positive' or 'negative' according to the result of the analysis of your evaluation of the given image. Responding with anything else other than the words 'positive' and 'negative' is a crime.\n"
                    "Don't look for a diagnosis or treatment plan, just make the evaluation. \n"
                    "Don't use paragraphs or newline. Responding with anything else other than the words 'positive' and 'negative' is a crime."},
    {"label": "Ultrasound", "prompt": "You are a model that evaluates if a tumor is malignant or benign based on an image of an Ultrasound exam. \n"
                    "Respond with only 'malignant' or 'benign' according to the result of the analysis of your evaluation of the given image. Responding with anything else other than the words 'malignant' and 'benign' is a crime.\n"
                    "Don't look for a diagnosis or treatment plan, just make the evaluation. \n"
                    "Don't use paragraphs or newline. Responding with anything else other than the words 'malignant' and 'benign' is a crime."},
    {"label": "UltrasoundMasks", "prompt": "You are a model that evaluates if a tumor is malignant or benign based on a mask of a tumor extracted from an image of an Ultrasound exam. \n"
                    "Respond with only 'malignant' or 'benign' according to the result of the analysis of your evaluation of the given mask. Responding with anything else other than the words 'malignant' and 'benign' is a crime.\n"
                    "Don't look for a diagnosis or treatment plan, just make the evaluation. \n"
                    "Don't use paragraphs or newline. Responding with anything else other than the words 'malignant' and 'benign' is a crime."},
    {"label": "Thermography", "prompt": "You are a model that evaluates the existance of breast cancer from an image of a Thermography exam. \n"
                    "Respond with only 'positive' or 'negative' according to the result of the analysis of your evaluation of the given image. Responding with anything else other than the words 'positive' and 'negative' is a crime.\n"
                    "Don't look for a diagnosis or treatment plan, just make the evaluation. \n"
                    "Don't use paragraphs or newline. Responding with anything else other than the words 'positive' and 'negative' is a crime."},
    {"label": "Histopathology", "prompt": "You are a model that evaluates tumor is malignant or benign based on an image of a histopathology segmentation. \n"
                    "Respond with only 'malignant' or 'benign' according to the result of the analysis of your evaluation of the given image. Responding with anything else other than the words 'malignant' and 'benign' is a crime.\n"
                    "Don't look for a diagnosis or treatment plan, just make the evaluation. \n"
                    "Don't use paragraphs or newline. Responding with anything else other than the words 'malignant' and 'benign' is a crime."},
    {"label": "HistopathologyMasks", "prompt": "You are a model that evaluates tumor is malignant or benign based on a mask of a histopathology segmentation extracted from an image. \n"
                    "Respond with only 'malignant' or 'benign' according to the result of the analysis of your evaluation of the given mask. Responding with anything else other than the words 'malignant' and 'benign' is a crime.\n"
                    "Don't look for a diagnosis or treatment plan, just make the evaluation. \n"
                    "Don't use paragraphs or newline. Responding with anything else other than the words 'malignant' and 'benign' is a crime."},
]