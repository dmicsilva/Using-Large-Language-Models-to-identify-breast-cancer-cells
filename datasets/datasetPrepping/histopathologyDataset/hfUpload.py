from huggingface_hub import HfApi

api = HfApi(token='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')
api.upload_folder(
    folder_path="/home/buybluepants/Documents/Using-Large-Language-Models-to-identify-breast-cancer-cells/datasets/datasetPrepping/histopathologyDataset/benign",
    repo_id="buybluepants/JSON_BreastCancerHistopathology",
    repo_type="dataset",
)