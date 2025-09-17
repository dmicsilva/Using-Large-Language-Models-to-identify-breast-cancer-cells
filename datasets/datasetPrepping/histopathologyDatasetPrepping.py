import os
import json
import datasetToJson

cwd = os.getcwd()

src_folder = 'datasets/breast-cancer-cell-segmentation-histopathology'

dest_malignant_images = os.path.join(cwd, 'datasets', 'datasetPrepping', 'histopathologyDataset', 'malignant')
dest_benign_images = os.path.join(cwd, 'datasets', 'datasetPrepping', 'histopathologyDataset', 'benign')

dest_malignant_masks = os.path.join(cwd, 'datasets', 'datasetPrepping', 'histopathologyMasksDataset', 'malignant')
dest_benign_masks = os.path.join(cwd, 'datasets', 'datasetPrepping', 'histopathologyMasksDataset', 'benign')

os.makedirs(dest_malignant_images, exist_ok=True)
os.makedirs(dest_benign_images, exist_ok=True)

os.makedirs(dest_malignant_masks, exist_ok=True)
os.makedirs(dest_benign_masks, exist_ok=True)

subfolders_to_process = ['Images', 'Masks']

for subfolder in subfolders_to_process:
    src_path = os.path.join(src_folder, subfolder)
    
    for filename in os.listdir(src_path):
        if filename.endswith(('.tif', '.TIF')):
            if 'malignant' in filename.lower():
                dest_filename = f"{os.path.splitext(filename)[0]}_malignant.tif"
                
                if subfolder == 'Images':
                    dest_file = os.path.join(dest_malignant_images, dest_filename)
                else:
                    dest_file = os.path.join(dest_malignant_masks, dest_filename)
            elif 'benign' in filename.lower():
                dest_filename = f"{os.path.splitext(filename)[0]}_benign.tif"
                
                if subfolder == 'Images':
                    dest_file = os.path.join(dest_benign_images, dest_filename)
                else:
                    dest_file = os.path.join(dest_benign_masks, dest_filename)

            src_file = os.path.join(src_path, filename)
            with open(src_file, 'rb') as src_f:
                with open(dest_file, 'wb') as dest_f:
                    dest_f.write(src_f.read())


dest_malignant_images = os.path.join(cwd, 'datasets', 'datasetPrepping', 'Json_histopathologyDataset', 'malignant')
dest_benign_images = os.path.join(cwd, 'datasets', 'datasetPrepping', 'Json_histopathologyDataset', 'benign')

dest_malignant_masks = os.path.join(cwd, 'datasets', 'datasetPrepping', 'Json_histopathologyMasksDataset', 'malignant')
dest_benign_masks = os.path.join(cwd, 'datasets', 'datasetPrepping', 'Json_histopathologyMasksDataset', 'benign')

os.makedirs(dest_malignant_images, exist_ok=True)
os.makedirs(dest_benign_images, exist_ok=True)

os.makedirs(dest_malignant_masks, exist_ok=True)
os.makedirs(dest_benign_masks, exist_ok=True)

subfolders_to_process = ['Images', 'Masks']

for subfolder in subfolders_to_process:
        src_path = os.path.join(src_folder, subfolder)
        
        for filename in os.listdir(src_path):
            if filename.endswith(('.tif', '.TIF')):
                src_file = os.path.join(src_path, filename)
                
                dest_filename = f"{os.path.splitext(filename)[0]}{'_benign' if 'benign' in filename.lower() else '_malignant'}{os.path.splitext(filename)[1]}"
                if (subfolder == 'Images' and 'benign' in filename.lower()):
                    dest_file = os.path.join(dest_benign_images, os.path.splitext(dest_filename)[0]) + '.json'
                if (subfolder == 'Images' and 'malignant' in filename.lower()):
                    dest_file = os.path.join(dest_malignant_images, os.path.splitext(dest_filename)[0]) + '.json'
                if (subfolder == 'Masks' and 'benign' in filename.lower()):
                    dest_file = os.path.join(dest_benign_masks, os.path.splitext(dest_filename)[0]) + '.json'
                if (subfolder == 'Masks' and 'malignant' in filename.lower()):
                    dest_file = os.path.join(dest_malignant_masks, os.path.splitext(dest_filename)[0]) + '.json'
                cancer_existance = "Malignant" if 'malignant' in filename else "Benign"

                base64_string = datasetToJson.image_to_base64(src_file)

                metadata = {
                    "base64_encoded_image": base64_string,
                    "cancerExistance": cancer_existance
                }

                with open(dest_file, 'w') as f:
                    json.dump(metadata, f, indent=4)