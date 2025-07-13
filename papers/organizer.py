import os
import re

# Define a dictionary of words to look for and their corresponding indexes
renaming_rules = {
    'mammography': '[Mammogram]',
    'mammogram': '[Mammogram]',
    'mammograms': '[Mammogram]',
    'thermograms': '[Thermogram]',
    'thermogram': '[Thermogram]',
    'thermography': '[Thermogram]',
    'thermographic': '[Thermogram]',
    'thermal': '[Thermogram]',
    'ultrasound': '[Ultrasound]',
    'ultrasounds': '[Ultrasound]',
    'tomosynthesis': '[Tomosynthesis]',
    'histopathology': '[Histopathology]',
    'histopathological': '[Histopathology]',
    'LLM': '[LLM]',
    'Large Language Models': '[LLM]',
    'Large Language Model': '[LLM]'
}

def rename_file(file_path):
    """
    Rename a file if it contains any of the specified words and has not been previously renamed.
    
    Args:
        file_path (str): Path to the file
    
    Returns:
        None
    """
    for word, index in renaming_rules.items():
        if re.search(word, os.path.basename(file_path), re.IGNORECASE):
            name, extension = os.path.splitext(os.path.basename(file_path))
            new_name = f'{index} {name}{extension}'
            
            # Check if file has already been renamed with the corresponding index
            existing_files = os.listdir()
            for existing_file in existing_files:
                if index in existing_file and \
                   (existing_file.replace(index, '').strip().lower() == name.lower()) and \
                   (os.path.splitext(existing_file)[1].lower() == os.path.splitext(new_name)[1].lower()):
                    print(f"Skipping file {file_path} as it has already been renamed to {new_name}")
                    return None

            # Get the original directory path
            original_dir = os.path.dirname(file_path)
            
            # Walk through the directory tree
            for root, dirs, files in os.walk(original_dir):
                for file_in_root in files:
                    if index in file_in_root and \
                       (file_in_root.replace(index, '').strip().lower() == name.lower()) and \
                       (os.path.splitext(file_in_root)[1].lower() == os.path.splitext(new_name)[1].lower()):
                        print(f"Skipping file {file_path} as it has already been renamed to {new_name}")
                        return None

            # If the new filename is not used, rename the original file
            print(f"Renaming {file_path} to {os.path.join(original_dir, new_name)}")
            os.rename(file_path, os.path.join(original_dir, new_name))
            return new_name

def main():
    for root, dirs, files in os.walk('.'):
        for file in files:
            if any(word.lower() in file.lower() for word in renaming_rules):
                rename_file(os.path.join(root, file))

if __name__ == "__main__":
    main()