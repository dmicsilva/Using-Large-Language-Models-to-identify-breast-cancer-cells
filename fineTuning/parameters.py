
datasets = [
    {"label": "MRI", "hugginFace": "buybluepants/BreastCancerCellsMRI/train", "splitTrain": False},
    {"label": "Mammogram", "hugginFace": "buybluepants/BreastCancerMammogram", "splitTrain": False},
    {"label": "Ultrasound", "hugginFace": "buybluepants/BreastCancerUltrasound", "splitTrain": True},
    {"label": "UltrasoundMasks", "hugginFace": "buybluepants/BreastCancerUltrasoundMasks", "splitTrain": True},
    {"label": "Thermography", "hugginFace": "buybluepants/BreastCancerThermogram", "splitTrain": True},
    {"label": "Histopathology", "hugginFace": "buybluepants/BreatCancerHistopathology", "splitTrain": True},
    {"label": "HistopathologyMasks", "hugginFace": "buybluepants/BreastCancerHistopatholgyMasks", "splitTrain": True}
]

models = [
    "unsloth/Llama-3.2-3B-Instruct"
]

instructions = [
    {"label": "MRI", "instruction": """You are an experienced physician that detects breast cancer in MRI images.
                                    Answer all the questions with the words "positive" or "negative" according to your evaluation of a given image.
                                    """},
    {"label": "Mammogram", "instruction": """You are an experienced physician that detects breast cancer in mammogram images.
                                    Answer all the questions with the words "positive" or "negative" according to your evaluation of a given image.
                                    """},
    {"label": "Ultrasound", "instruction": """You are an experienced physician that detects if a breast mass is malignant ou benign, in ultrasound images.
                                    Answer all the questions with the words "malignant" or "benign" according to your evaluation of a given image.
                                    """},
    {"label": "UltrasoundMasks", "instruction": """You are an experienced physician that detects if a breast mass is malignant ou benign, in masks extrated from ultrasound images.
                                    Answer all the questions with the words "malignant" or "benign" according to your evaluation of a given image.
                                    """},
    {"label": "Thermography", "instruction": """You are an experienced physician that detects breast cancer in thermography images.
                                    Answer all the questions with the words "positive" or "negative" according to your evaluation of a given image.
                                    """},
    {"label": "Histopathology", "instruction": """You are an experienced physician that detects if a segmentation of cells is malignant ou benign, in histopathology images.
                                    Answer all the questions with the words "malignant" or "benign" according to your evaluation of a given image.
                                    """},
    {"label": "HistopathologyMasks", "instruction": """You are an experienced physician that detects if a segmentation of cells is malignant ou benign, in masks extrated from histopathology images.
                                    Answer all the questions with the words "malignant" or "benign" according to your evaluation of a given image.
                                    """},
]