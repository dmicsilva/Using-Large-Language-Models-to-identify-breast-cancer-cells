
datasets = [
    {"label": "MRI", "hugginFace": "buybluepants/JSON_BreastCancerMRI", "splitTrain": False},
    {"label": "Mammogram", "hugginFace": "buybluepants/JSON_BreastCancerMammogram", "splitTrain": False},
    {"label": "Ultrasound", "hugginFace": "buybluepants/JSON_BreastCancerUltrasound", "splitTrain": True},
    {"label": "Thermography", "hugginFace": "buybluepants/JSON_BreastCancerThermogram", "splitTrain": True},
    {"label": "Histopathology", "hugginFace": "buybluepants/JSON_BreatCancerHistopathology", "splitTrain": True},
]

models = [
    "unsloth/Llama-3.2-3B-Instruct",
    "microsoft/Phi-3-mini-128k-instruct",
    "dphn/Dolphin-Llama3-8B-Instruct-exl2-6bpw",
    "openchat/openchat_3.5",
    "Qwen/Qwen2.5-0.5B-Instruct",
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
]

instructions = [
    {"label": "MRI", "instruction": """You are an experienced physician that detects breast cancer in MRI images.
                                    Answer all the questions with the words "positive" or "negative" according to your evaluation of a given image.
                                    """},
    {"label": "Mammogram", "instruction": """You are an experienced physician that detects breast cancer in mammogram images.
                                    Answer all the questions with the words "positive" or "negative" according to your evaluation of a given image.
                                    """},
    {"label": "Ultrasound", "instruction": """You are an experienced physician that detects if a breast mass is malignant ou benign, in ultrasound images and masks extracted from images.
                                    Answer all the questions with the words "malignant" or "benign" according to your evaluation of a given image.
                                    """},
    {"label": "Thermography", "instruction": """You are an experienced physician that detects breast cancer in thermography images.
                                    Answer all the questions with the words "positive" or "negative" according to your evaluation of a given image.
                                    """},
    {"label": "Histopathology", "instruction": """You are an experienced physician that detects if a segmentation of cells is malignant ou benign, in histopathology images and masks extracted from images.
                                    Answer all the questions with the words "malignant" or "benign" according to your evaluation of a given image.
                                    """},
]