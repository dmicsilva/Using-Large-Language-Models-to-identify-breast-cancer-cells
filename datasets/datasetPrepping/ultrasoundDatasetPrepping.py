import pandas as pd
import os

classificationSheetPath = os.path.join(cwd, 'datasets/datasetPrepping', 'BrEaST-Lesions-USG-clinical-data-Dec-15-2023.xlsx')
df = pd.read_excel(classificationSheetPath)
base_directory_path = os.path.join(cwd, 'datasets/BrEaST-Lesions_USG-images_and_masks')

if not os.path.exists(base_directory_path):
    print(f"Directory {base_directory_path} does not exist.")
else:
    ultrasound_masks_dir = os.path.join(base_directory_path, 'ultrasoundMasks')
    ultrasound_dir = os.path.join(base_directory_path, 'ultrasound')

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

    for filename in os.listdir(base_directory_path):
        if '_tumor.png' in filename:
            path = os.path.join(base_directory_path, filename)
            image_column_name = [column for column in df.columns if 'Mask_tumor_filename' in column][0]
            classification_match = df.loc[df[image_column_name] == filename]
            
            if (not classification_match.empty):
                classification = classification_match['Classification'].iloc[0]
                new_filename = f"{os.path.splitext(filename)[0]}_{classification}.png"
                
                destination_path = os.path.join(dir_path_malignant_masks, new_filename)
                if classification.lower() == 'benign':
                    destination_path = os.path.join(dir_path_benign_masks, new_filename)
                    
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
                
                destination_path = os.path.join(dir_path_benign_ultrasound, new_filename)
                if classification.lower() == 'malignant':
                    destination_path = os.path.join(dir_path_malignant_ultrasound, new_filename)
                    
                os.rename(path, destination_path)
            else:
                print(f"No match found for file {filename}")