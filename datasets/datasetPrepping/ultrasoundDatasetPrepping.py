import pandas as pd
import os
import json
import datasetToJson

cwd = os.getcwd()

classificationSheetPath = os.path.join(cwd, 'datasets/datasetPrepping', 'BrEaST-Lesions-USG-clinical-data-Dec-15-2023.xlsx')
df = pd.read_excel(classificationSheetPath)
base_directory_path = os.path.join(cwd, 'datasets/BrEaST-Lesions_USG-images_and_masks')

if not os.path.exists(base_directory_path):
    print(f"Directory {base_directory_path} does not exist.")
else:
    ultrasound_masks_dir = os.path.join(cwd, 'datasets', 'datasetPrepping', 'ultrasoundMasksDataset')
    ultrasound_dir = os.path.join(cwd, 'datasets', 'datasetPrepping', 'ultrasoundDataset')

    dir_path_malignant_masks = os.path.join(ultrasound_masks_dir, 'malignant')
    dir_path_benign_masks = os.path.join(ultrasound_masks_dir, 'benign')
    dir_path_malignant_ultrasound = os.path.join(ultrasound_dir, 'malignant')
    dir_path_benign_ultrasound = os.path.join(ultrasound_dir, 'benign')

    os.makedirs(ultrasound_masks_dir, exist_ok=True)
    os.makedirs(dir_path_malignant_masks, exist_ok=True)
    os.makedirs(dir_path_benign_masks, exist_ok=True)
    os.makedirs(ultrasound_dir, exist_ok=True)
    os.makedirs(dir_path_malignant_ultrasound, exist_ok=True)
    os.makedirs(dir_path_benign_ultrasound, exist_ok=True)

    json_ultrasound_masks_dir = os.path.join(cwd, 'datasets', 'datasetPrepping', 'Json_ultrasoundMasksDataset')
    json_ultrasound_dir = os.path.join(cwd, 'datasets', 'datasetPrepping', 'Json_ultrasoundDataset')

    json_dir_path_malignant_masks = os.path.join(json_ultrasound_masks_dir, 'malignant')
    json_dir_path_benign_masks = os.path.join(json_ultrasound_masks_dir, 'benign')
    json_dir_path_malignant_ultrasound = os.path.join(json_ultrasound_dir, 'malignant')
    json_dir_path_benign_ultrasound = os.path.join(json_ultrasound_dir, 'benign')

    os.makedirs(json_ultrasound_masks_dir, exist_ok=True)
    os.makedirs(json_dir_path_malignant_masks, exist_ok=True)
    os.makedirs(json_dir_path_benign_masks, exist_ok=True)
    os.makedirs(json_ultrasound_dir, exist_ok=True)
    os.makedirs(json_dir_path_malignant_ultrasound, exist_ok=True)
    os.makedirs(json_dir_path_benign_ultrasound, exist_ok=True)

    for filename in os.listdir(base_directory_path):
        src_file = os.path.join(base_directory_path, filename)
        if '_tumor.png' in filename:
            path = os.path.join(base_directory_path, filename)
            image_column_name = [column for column in df.columns if 'Mask_tumor_filename' in column][0]
            classification_match = df.loc[df[image_column_name] == filename]
            
            if (not classification_match.empty):
                classification = classification_match['Classification'].iloc[0]
                new_filename = f"{os.path.splitext(filename)[0]}_{classification}.png"
                json_new_filename = f"{os.path.splitext(filename)[0]}_{classification}.json"
                
                destination_path = os.path.join(dir_path_malignant_masks, new_filename)
                json_destination_path = os.path.join(json_dir_path_malignant_masks, json_new_filename)
                if classification.lower() == 'benign':
                    destination_path = os.path.join(dir_path_benign_masks, new_filename)
                    json_destination_path = os.path.join(json_dir_path_benign_masks, json_new_filename)
                
                base64_string = datasetToJson.image_to_base64(src_file)

                metadata = {
                    "base64_encoded_image": base64_string,
                    "cancerExistance": classification
                }
    
                with open(json_destination_path, 'w') as f:
                    json.dump(metadata, f, indent=4)
                    
                os.rename(path, destination_path)
            else:
                print(f"No match found for file {filename}")

        else:
            path = os.path.join(base_directory_path, filename)
            image_column_name = [column for column in df.columns if 'Image_filename' in column][0]
            classification_match = df.loc[df[image_column_name] == filename]

            if (not classification_match.empty):
                classification = classification_match['Classification'].iloc[0]
                new_filename = f"{os.path.splitext(filename)[0]}_{classification}.png"
                json_new_filename = f"{os.path.splitext(filename)[0]}_{classification}.json"

                destination_path = os.path.join(dir_path_benign_ultrasound, new_filename)
                json_destination_path = os.path.join(json_dir_path_benign_ultrasound, json_new_filename)
                if classification.lower() == 'malignant':
                    destination_path = os.path.join(dir_path_malignant_ultrasound, new_filename)
                    json_destination_path = os.path.join(json_dir_path_malignant_ultrasound, json_new_filename)
                
                base64_string = datasetToJson.image_to_base64(src_file)

                metadata = {
                    "base64_encoded_image": base64_string,
                    "cancerExistance": classification
                }
    
                with open(json_destination_path, 'w') as f:
                    json.dump(metadata, f, indent=4)
                    
                os.rename(path, destination_path)
            else:
                print(f"No match found for file {filename}")
                if 'other' in filename:
                    new_filename = f"{os.path.splitext(filename)[0]}_benign.png"
                    json_new_filename = f"{os.path.splitext(filename)[0]}_benign.json"
                    destination_path = os.path.join(dir_path_benign_ultrasound, new_filename)
                    json_destination_path = os.path.join(json_dir_path_benign_ultrasound, json_new_filename)

                    base64_string = datasetToJson.image_to_base64(src_file)

                    metadata = {
                        "base64_encoded_image": base64_string,
                        "cancerExistance": "benign"
                    }
        
                    with open(json_destination_path, 'w') as f:
                        json.dump(metadata, f, indent=4)
                        
                    os.rename(path, destination_path)