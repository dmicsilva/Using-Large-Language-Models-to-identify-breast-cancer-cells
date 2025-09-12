datasets = [
    {"label": "MRI", "hugginFace": "buybluepants/BreastCancerCellsMRI/train"},
    {"label": "Mammogram", "hugginFace": "buybluepants/BreastCancerMammogram"},
    {"label": "Ultrasound", "hugginFace": "buybluepants/BreastCancerUltrasound"},
    {"label": "UltrasoundMasks", "hugginFace": "buybluepants/BreastCancerUltrasoundMasks"},
    {"label": "Thermography", "hugginFace": "buybluepants/BreastCancerThermogram"},
    {"label": "Histopathology", "hugginFace": "buybluepants/BreastCancerHistopathology"},
    {"label": "HistopathologyMasks", "hugginFace": "buybluepants/BreastCancerHistopathologyMasks"},
]

models = [
    "unsloth/Llama-3.2-3B-Instruct"
]

instructions = [
    {"label": "MRI", "instruction": "buybluepants/BreastCancerCellsMRI/train"},
    {"label": "Mammogram", "instruction": "buybluepants/BreastCancerMammogram"},
    {"label": "Ultrasound", "instruction": "buybluepants/BreastCancerUltrasound"},
    {"label": "UltrasoundMasks", "instruction": "buybluepants/BreastCancerUltrasoundMasks"},
    {"label": "Thermography", "instruction": "buybluepants/BreastCancerThermogram"},
    {"label": "Histopathology", "instruction": "buybluepants/BreastCancerHistopathology"},
    {"label": "HistopathologyMasks", "instruction": "buybluepants/BreastCancerHistopathologyMasks"},
]