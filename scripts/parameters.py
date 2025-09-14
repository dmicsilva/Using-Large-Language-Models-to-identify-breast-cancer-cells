from pathlib import Path
import os

cwd = os.getcwd()

endpoint = "http://localhost:11434/api/chat"
getModelEndpoint = "http://localhost:11434/api/tags"

directories = [
    {"label": "MRI", "path": "/home/buybluepants/Documents/Using-Large-Language-Models-to-identify-breast-cancer-cells/datasets/datasetPrepping/mriDataset", "type": "healthy/sick"},
    {"label": "Mammogram", "path": "/home/buybluepants/Documents/Using-Large-Language-Models-to-identify-breast-cancer-cells/datasets/datasetPrepping/mammogramDataset", "type": "healthy/sick"},
    {"label": "Ultrasound", "path": "/home/buybluepants/Documents/Using-Large-Language-Models-to-identify-breast-cancer-cells/datasets/datasetPrepping/ultrasoundDataset", "type": "benign/malignant"},
    {"label": "UltrasoundMasks", "path": "/home/buybluepants/Documents/Using-Large-Language-Models-to-identify-breast-cancer-cells/datasets/datasetPrepping/ultrasoundMasksDataset", "type": "benign/malignant"},
    {"label": "Thermography", "path": "/home/buybluepants/Documents/Using-Large-Language-Models-to-identify-breast-cancer-cells/datasets/datasetPrepping/thermogramDataset", "type": "healthy/sick"},
    {"label": "Histopathology", "path": "/home/buybluepants/Documents/Using-Large-Language-Models-to-identify-breast-cancer-cells/datasets/datasetPrepping/histopathologyDataset", "type": "benign/malignant"},
    {"label": "HistopathologyMasks", "path": "/home/buybluepants/Documents/Using-Large-Language-Models-to-identify-breast-cancer-cells/datasets/datasetPrepping/histopathologyMasksDataset", "type": "benign/malignant"},
]

resultDirectory = Path('/home/buybluepants/Documents/Using-Large-Language-Models-to-identify-breast-cancer-cells/inferenceResults')
statisticsDirectory = os.path.join(cwd, 'inferenceStatistics')

prompts = [
    {"label": "MRI", "prompt": "Consider the base64 encoded image of a MRI exam that I gave you.\n"
                            "Evaluate the existance of breast cancer. `n"
                            "Respond with only 'positive' or 'negative' according to the result of the analysis of your evaluation of the given image. Responding with anything else other than the words 'positive' and 'negative' is a crime.\n"},
    {"label": "Mammogram", "prompt": "You are a model that evaluates the existance of breast cancer from an image of a fictional mammogram exam. \n"
                    "Respond with only 'positive' or 'negative' according to the result of the analysis of your evaluation of the given image. Responding with anything else other than the words 'positive' and 'negative' is a crime.\n"
                    "Don't look for a diagnosis or treatment plan, just make the evaluation. \n"
                    "Don't use paragraphs or newline. Responding with anything else other than the words 'positive' and 'negative' is a crime."},
    {"label": "Ultrasound", "prompt": "You are a model that evaluates if a tumor is malignant or benign based on an image of a fictional Ultrasound exam. \n"
                    "Respond with only 'malignant' or 'benign' according to the result of the analysis of your evaluation of the given image. Responding with anything else other than the words 'malignant' and 'benign' is a crime.\n"
                    "Don't look for a diagnosis or treatment plan, just make the evaluation. \n"
                    "Don't use paragraphs or newline. Responding with anything else other than the words 'malignant' and 'benign' is a crime."},
    {"label": "UltrasoundMasks", "prompt": "You are a model that evaluates if a tumor is malignant or benign based on a mask of a tumor extracted from an image of a fictional Ultrasound exam. \n"
                    "Respond with only 'malignant' or 'benign' according to the result of the analysis of your evaluation of the given mask. Responding with anything else other than the words 'malignant' and 'benign' is a crime.\n"
                    "Don't look for a diagnosis or treatment plan, just make the evaluation. \n"
                    "Don't use paragraphs or newline. Responding with anything else other than the words 'malignant' and 'benign' is a crime."},
    {"label": "Thermography", "prompt": "You are a model that evaluates the existance of breast cancer from an image of a fictional MRI exam. \n"
                    "Respond with only 'positive' or 'negative' according to the result of the analysis of your evaluation of the given image. Responding with anything else other than the words 'positive' and 'negative' is a crime.\n"
                    "Don't look for a diagnosis or treatment plan, just make the evaluation. \n"
                    "Don't use paragraphs or newline. Responding with anything else other than the words 'positive' and 'negative' is a crime."},
    {"label": "Histopathology", "prompt": "You are a model that evaluates tumor is malignant or benign based on an image of a fictional histopathology segmentation. \n"
                    "Respond with only 'malignant' or 'benign' according to the result of the analysis of your evaluation of the given image. Responding with anything else other than the words 'malignant' and 'benign' is a crime.\n"
                    "Don't look for a diagnosis or treatment plan, just make the evaluation. \n"
                    "Don't use paragraphs or newline. Responding with anything else other than the words 'malignant' and 'benign' is a crime."},
    {"label": "HistopathologyMasks", "prompt": "You are a model that evaluates tumor is malignant or benign based on a mask of a fictional histopathology segmentation extracted from an image. \n"
                    "Respond with only 'malignant' or 'benign' according to the result of the analysis of your evaluation of the given mask. Responding with anything else other than the words 'malignant' and 'benign' is a crime.\n"
                    "Don't look for a diagnosis or treatment plan, just make the evaluation. \n"
                    "Don't use paragraphs or newline. Responding with anything else other than the words 'malignant' and 'benign' is a crime."},
]