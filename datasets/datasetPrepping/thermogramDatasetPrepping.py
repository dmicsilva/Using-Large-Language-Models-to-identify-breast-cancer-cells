import os

cwd = os.getcwd()

src_folder = 'datasets/BCD_Dataset-thermogram'
"""
dest_healthy = os.path.join(cwd, 'thermogramDataset', 'healthy')
dest_sick = os.path.join(cwd, 'thermogramDataset', 'sick')

os.makedirs(dest_healthy, exist_ok=True)
os.makedirs(dest_sick, exist_ok=True)

subfolders_to_process = ['normal', 'Sick']

for subfolder in subfolders_to_process:
    src_path = os.path.join(src_folder, subfolder)
    
    for filename in os.listdir(src_path):
        src_file = os.path.join(src_path, filename)
        
        dest_filename = f"{os.path.splitext(filename)[0]}{'_healthy' if subfolder == 'normal' else '_sick'}{os.path.splitext(filename)[1]}"
        dest_file = os.path.join(dest_sick if subfolder == 'Sick' else dest_healthy, dest_filename)

        with open(src_file, 'rb') as src_f:
            with open(dest_file, 'wb') as dest_f:
                dest_f.write(src_f.read())
"""
dest_healthy = os.path.join(cwd, 'datasets', 'datasetPrepping', 'Json_thermogramDataset', 'healthy')
dest_sick = os.path.join(cwd, 'datasets', 'datasetPrepping', 'Json_thermogramDataset', 'sick')

os.makedirs(dest_healthy, exist_ok=True)
os.makedirs(dest_sick, exist_ok=True)

subfolders_to_process = ['normal', 'Sick']

for subfolder in subfolders_to_process:
        src_path = os.path.join(src_folder, subfolder)
        
        for filename in os.listdir(src_path):
            src_file = os.path.join(src_path, filename)
            
            dest_filename = f"{os.path.splitext(filename)[0]}{'_healthy' if subfolder == 'normal' else '_sick'}{os.path.splitext(filename)[1]}"
            dest_file = os.path.join(dest_sick if subfolder == 'Sick' else dest_healthy, dest_filename)

            with open(src_file, 'rb') as src_f:
                with open(dest_file, 'wb') as dest_f:
                    dest_f.write(src_f.read())