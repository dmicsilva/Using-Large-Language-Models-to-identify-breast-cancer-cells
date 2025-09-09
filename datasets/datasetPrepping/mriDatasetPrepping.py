import os

cwd = os.getcwd()

src_folder = 'datasets/Breast Cancer Patients MRI\'s'

dest_healthy = os.path.join(cwd, 'mriDataset', 'healthy')
dest_sick = os.path.join(cwd, 'mriDataset', 'sick')

os.makedirs(dest_healthy, exist_ok=True)
os.makedirs(dest_sick, exist_ok=True)

subfolders_to_process = ['Healthy', 'Sick']

for subfolder in subfolders_to_process:
    src_path = os.path.join(src_folder, 'validation', subfolder)
    
    for filename in os.listdir(src_path):
        src_file = os.path.join(src_path, filename)
        
        dest_filename = f"{os.path.splitext(filename)[0]}{'_healthy' if subfolder == 'Healthy' else '_sick'}{os.path.splitext(filename)[1]}"
        dest_file = os.path.join(dest_sick if subfolder == 'Sick' else dest_healthy, dest_filename)

        with open(src_file, 'rb') as src_f:
            with open(dest_file, 'wb') as dest_f:
                dest_f.write(src_f.read())