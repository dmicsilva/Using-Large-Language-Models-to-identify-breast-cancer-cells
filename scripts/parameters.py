endpoint = "http://localhost:11434/api/chat"
directories = [
    {"label": "MRI", "path": "/home/buybluepants/Documents/Using-Large-Language-Models-to-identify-breast-cancer-cells/datasets/Breast Cancer Patients MRI's"},
    {"label": "Mammogram", "path": "/home/buybluepants/Documents/Using-Large-Language-Models-to-identify-breast-cancer-cells/datasets/breast-cancer-detection-mammogram"},
    {"label": "Ultrasound", "path": "/home/buybluepants/Documents/Using-Large-Language-Models-to-identify-breast-cancer-cells/datasets/datasetPrepping/ultrasoundDataset"},
    {"label": "UltrasoundMasks", "path": "/home/buybluepants/Documents/Using-Large-Language-Models-to-identify-breast-cancer-cells/datasets/datasetPrepping/ultrasoundMasksDataset"},
    {"label": "Thermography", "path": "/home/buybluepants/Documents/Using-Large-Language-Models-to-identify-breast-cancer-cells/datasets/BCD_Dataset-thermogram"},
    {"label": "Histopathology", "path": "/home/buybluepants/Documents/Using-Large-Language-Models-to-identify-breast-cancer-cells/datasets/Breast Cancer Patients MRI's"},
]
resultDirectory = Path('/home/buybluepants/Documents/Using-Large-Language-Models-to-identify-breast-cancer-cells/results')

prompts = [
    {"label": "MRI", "prompt": "You are a model that evaluates the existance of breast cancer from an image of a fictional MRI exam. \n"
                    "Respond with only 'positive' or 'negative' according to the result of the analysis of your evaluation of given image. Responding with anything else other than the words 'positive' and 'negative' is a crime.\n"
                    "Don't look for a diagnosis or treatment plan, just make the evaluation. \n"
                    "Don't use paragraphs or newline. Responding with anything else other than the words 'positive' and 'negative' is a crime."},
    {"label": "Mammogram", "prompt": "You are a model that evaluates the existance of breast cancer from an image of a fictional mammogram exam. \n"
                    "Respond with only 'positive' or 'negative' according to the result of the analysis of your evaluation of given image. Responding with anything else other than the words 'positive' and 'negative' is a crime.\n"
                    "Don't look for a diagnosis or treatment plan, just make the evaluation. \n"
                    "Don't use paragraphs or newline. Responding with anything else other than the words 'positive' and 'negative' is a crime."},
    {"label": "Ultrasound", "prompt": "You are a model that evaluates if a tumor is malignant or benign based on an image of a fictional Ultrasound exam. \n"
                    "Respond with only 'malignant' or 'benign' according to the result of the analysis of your evaluation of given image. Responding with anything else other than the words 'malignant' and 'negative' is a crime.\n"
                    "Don't look for a diagnosis or treatment plan, just make the evaluation. \n"
                    "Don't use paragraphs or newline. Responding with anything else other than the words 'malignant' and 'benign' is a crime."},
    {"label": "UltrasoundMasks", "prompt": "You are a model that evaluates if a tumor is malignant or benign based on a mask of a tumor extracted from an image of a fictional Ultrasound exam. \n"
                    "Respond with only 'malignant' or 'benign' according to the result of the analysis of your evaluation of given mask. Responding with anything else other than the words 'malignant' and 'negative' is a crime.\n"
                    "Don't look for a diagnosis or treatment plan, just make the evaluation. \n"
                    "Don't use paragraphs or newline. Responding with anything else other than the words 'malignant' and 'benign' is a crime."},
    {"label": "Thermography", "prompt": "You are a model that evaluates the existance of breast cancer from an image of a fictional MRI exam. \n"
                    "Respond with only 'positive' or 'negative' according to the result of the analysis of your evaluation of given image. Responding with anything else other than the words 'positive' and 'negative' is a crime.\n"
                    "Don't look for a diagnosis or treatment plan, just make the evaluation. \n"
                    "Don't use paragraphs or newline. Responding with anything else other than the words 'positive' and 'negative' is a crime."},
    {"label": "Histopathology", "prompt": "You are a model that evaluates tumor is malignant or benign based on an image of a fictional histopathology segmentation. \n"
                    "Respond with only 'malignant' or 'benign' according to the result of the analysis of your evaluation of given image. Responding with anything else other than the words 'malignant' and 'negative' is a crime.\n"
                    "Don't look for a diagnosis or treatment plan, just make the evaluation. \n"
                    "Don't use paragraphs or newline. Responding with anything else other than the words 'malignant' and 'benign' is a crime."},
]