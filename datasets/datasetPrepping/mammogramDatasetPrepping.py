import os
import datasetToJson
import json

cwd = os.getcwd()

src_folder = 'datasets/breast-cancer-detection-mammogram'

dest_healthy = os.path.join(cwd, 'datasets', 'datasetPrepping', 'mammogramDataset', 'healthy')
dest_sick = os.path.join(cwd, 'datasets', 'datasetPrepping', 'mammogramDataset', 'sick')

os.makedirs(dest_healthy, exist_ok=True)
os.makedirs(dest_sick, exist_ok=True)

subfolders_to_process = ['test', 'valid']
sub_subfolders_to_process = ['0', '1']

for subfolder in subfolders_to_process:
    for sub_subfolder in sub_subfolders_to_process:
        src_path = os.path.join(src_folder, subfolder, sub_subfolder)
        
        for filename in os.listdir(src_path):
            src_file = os.path.join(src_path, filename)
            
            dest_filename = f"{os.path.splitext(filename)[0]}{'_healthy' if sub_subfolder == '0' else '_sick'}{os.path.splitext(filename)[1]}"
            dest_file = os.path.join(dest_sick if sub_subfolder == '1' else dest_healthy, dest_filename)

            with open(src_file, 'rb') as src_f:
                with open(dest_file, 'wb') as dest_f:
                    dest_f.write(src_f.read())


dest_healthy = os.path.join(cwd, 'datasets', 'datasetPrepping', 'Json_mammogramDataset', 'healthy')
dest_sick = os.path.join(cwd, 'datasets', 'datasetPrepping', 'Json_mammogramDataset', 'sick')

os.makedirs(dest_healthy, exist_ok=True)
os.makedirs(dest_sick, exist_ok=True)

subfolders_to_process = ['train']
sub_subfolders_to_process = ['0', '1']

for subfolder in subfolders_to_process:
    for sub_subfolder in sub_subfolders_to_process:
        src_path = os.path.join(src_folder, subfolder, sub_subfolder)
        
        for filename in os.listdir(src_path):
            src_file = os.path.join(src_path, filename)
            
            dest_filename = f"{os.path.splitext(filename)[0]}{'_healthy' if sub_subfolder == '0' else '_sick'}{os.path.splitext(filename)[1]}"
            dest_file = os.path.join(dest_sick if sub_subfolder == '1' else dest_healthy, os.path.splitext(dest_filename)[0]) + '.json'
            cancer_existance = "Negative" if sub_subfolder == '0' else "Positive"

            base64_string = datasetToJson.image_to_base64(src_file)

            metadata = {
                "base64_encoded_image": base64_string,
                "cancerExistance": cancer_existance
            }

            with open(dest_file, 'w') as f:
                json.dump(metadata, f, indent=4)
