import pandas as pd
import os

# Read Excel file
df = pd.read_excel('/home/buybluepants/Documents/Using-Large-Language-Models-to-identify-breast-cancer-cells/datasets/datasetPrepping/BrEaST-Lesions-USG-clinical-data-Dec-15-2023.xlsx')

# Specify base directory path
base_directory_path = '/home/buybluepants/Documents/Using-Large-Language-Models-to-identify-breast-cancer-cells/datasets/BrEaST-Lesions_USG-images_and_masks'

if not os.path.exists(base_directory_path):
    print(f"Directory {base_directory_path} does not exist.")
else:
    # Create folders in specified base directory
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

    # Iterate over files in directory
    for filename in os.listdir(base_directory_path):
        # Check if the file has the 'tumor' suffix
        if '_tumor.png' in filename:
            path = os.path.join(base_directory_path, filename)
            image_column_name = [column for column in df.columns if 'CaseID' in column or 'id' in column][0]
            classification_match = df.loc[df['Mask_tumor_filename'] == os.path.splitext(filename)[0]]
            
            # Check if there is a match
            if not classification_match.empty:
                classification = classification_match['Classification'].iloc[0]
                new_filename = f"{os.path.splitext(filename)[0]}_{classification}.png"
                
                # Move file to corresponding folder
                destination_path = os.path.join(dir_path_malignant_masks, new_filename)
                if classification.lower() == 'benign':
                    destination_path = os.path.join(dir_path_benign_masks, new_filename)
                    
                os.rename(path, destination_path)
            else:
                print(f"No match found for file {filename}")
        else:
            path = os.path.join(base_directory_path, filename)
            image_column_name = [column for column in df.columns if 'CaseID' in column or 'id' in column][0]
            classification_match = df.loc[df['Image_filename'] == os.path.splitext(filename)[0]]
            
            # Check if there is a match
            if not classification_match.empty:
                classification = classification_match['Classification'].iloc[0]
                new_filename = f"{os.path.splitext(filename)[0]}_{classification}.png"
                
                # Move file to corresponding folder
                destination_path = os.path.join(dir_path_benign_ultrasound, new_filename)
                if classification.lower() == 'malignant':
                    destination_path = os.path.join(dir_path_malignant_ultrasound, new_filename)
                    
                os.rename(path, destination_path)
            else:
                print(f"No match found for file {filename}")