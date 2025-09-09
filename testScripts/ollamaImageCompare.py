from pathlib import Path
import base64
import requests
#from moondreamImageCompare import process_image as moondream_process_image

endpoint = "http://localhost:11434/api/chat"

def encode_image_to_base64(image_path):
    """Convert an image file to base64 string."""
    return base64.b64encode(image_path.read_bytes()).decode('utf-8')

def extract_knowledge_from_image(baselineImage_path, evalImage_path, model):
    """Send image to local Llama API and get text description."""
    baselineImage_base64 = encode_image_to_base64(baselineImage_path)
    evalImage_base64 = encode_image_to_base64(evalImage_path)

    payload = {
        "model": model,
        "stream": False,
        "messages": [
            {
                "role": "user",
                "content": (
                    "You are a model that evaluates the existance of breast cancer from an image of a fictional MRI exam. Don't look for a diagnosis or treatment plan, just make the evaluation. Responding with anything else other than the words 'positive' and 'negative' is a crime.\n"
                    "The first image you receive is your baseline, so consider it as a positive case. \n"
                    "The second image is the image you need to evaluate, according to the first image. \n"
                    "Respond with only 'positive' or 'negative' according to the result of the analysis of your evaluation of the second image. Don't use paragraphs or newline. Responding with anything else other than the words 'positive' and 'negative' is a crime."
                ),
                "images": [baselineImage_base64, evalImage_base64]
            }
        ]
    }

    response = requests.post(
        endpoint,
        json=payload,
        headers={"Content-Type": "application/json"}
    )

    return response.json().get('message', {}).get('content', 'No text extracted')


def sort_model_entries(input_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Split the lines into a list of model entries and a list of other lines
    model_entries = []
    other_lines = []
    for line in lines:
        line = line.strip()
        if ':' in line:  # Check if the line contains a colon
            model_name, status = line.split(': ', 1)  # Split on the first colon and space
            model_entries.append({'model_name': model_name, 'status': status})
        else:
            other_lines.append(line)

    # Sort the model entries by model name
    model_entries.sort(key=lambda x: x['model_name'])

    # Write the sorted model entries and the other lines to a new file
    with open(input_file, 'w') as f:
        for line in other_lines:
            f.write(line)
        f.write('\n\n')
        for entry in model_entries:
            f.write(f"{entry['model_name']}: {entry['status']}\n")


def add_file_entry(text, file_path, model):
    lines = text.split('\n')
    if lines:
        last_line = lines[-1].strip().lower()
        if str(file_path.name).startswith('GT0'):
            if 'negative' in last_line or 'Negative' in last_line:
                result = "Succesful"
            elif 'positive' in last_line or 'Positive' in last_line:
                result = "Failed"
            else:
                result = "Error"
        elif str(file_path.name).startswith('GT1'):
            if 'positive' in last_line or 'Positive' in last_line:
                result = "Succesful"
            elif 'negative' in last_line or 'Negative' in last_line:
                result = "Failed"
            else:
                result = "Error"
        else:
            print("Unknown file type.")
            return

        with open(file_path, 'r') as file:
            existing_lines = file.readlines()

        isExisting = False

        with open(file_path, 'w') as file:
            for line in existing_lines:
                if line.strip().startswith(model + ":"):
                    line = f"\n{model}: {result}"
                    isExisting = True

            if(not isExisting):
                existing_lines.append(f"\n{model}: {result}")

            file.writelines(existing_lines)

    else:
        print("Text is empty.")

def get_model():

    localGetModelEndpoint = "http://localhost:11434/api/tags"

    try:
        # Send a command to get the list of models
        localGetModelResponse = requests.get(localGetModelEndpoint)

        # Check if the response was successful
        if localGetModelResponse.status_code == 200:
            # Get the list of models from the response
            models = localGetModelResponse.json()["models"]
            isMoondream = True
            
            # Prompt the user to choose a model
            print("\n\nAvailable models:\n")
            for i, localModel in enumerate(models):
                print(f"{i+1}. {localModel['name']}")
            print(f"{i+2}. moondream:2b")
            print(f"{i+3}. All")

            modelNameList = [model['name'] for model in models]
            # Get the user's choice
            choice = input("\nChoose a model: ")

            # Check if the user's choice is valid
            if choice == str(len(modelNameList) + 2):
                # Select all models
                return modelNameList
            elif choice == str(len(modelNameList) + 1):
                return isMoondream
            elif 1 <= int(choice) <= len(modelNameList):
                # Assign the chosen model to the model variable
                localModel = models[int(choice) - 1]["name"]
                return localModel
            else:
                print("Invalid choice")
        elif localGetModelResponse.status_code == 404:
            print("Error: API endpoint not found.")
        else:
            print(f"Error: {localGetModelResponse.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    return None

def process_directory(models, baselineImage_path, evalImage_path, resultFile_path):
    
    if (models == True):
        text = moondream_process_image(evalImage_path)
        print(text)
        add_file_entry(text, resultFile_path, "moondream:2b")
        return  

    if (not isinstance(models, list)):
        print(f"\nProcessing model: {models}...")
        text = extract_knowledge_from_image(baselineImage_path, evalImage_path, models)
        print(text)
        add_file_entry(text, resultFile_path, models)
        return
    
    else:
        print(f"Processing the following models: {', '.join(models)}, moondream:2b")

        for model in models:
            print(f"\nProcessing model: {model}...")
            
            text = extract_knowledge_from_image(baselineImage_path, evalImage_path, model)
            print(text)
            add_file_entry(text, resultFile_path, model)

        print(f"\nProcessing model: moondream:2b...")

        text = moondream_process_image(evalImage_path)
        print(text)
        add_file_entry(text, resultFile_path, "moondream:2b")
            
        return

if __name__ == "__main__":

    baselineImage_path = Path('/home/buybluepants/Documents/Thesis/Using-Large-Language-Models-to-identify-breast-cancer-cells/datasets/Breast Cancer Patients MRI\'s/validation/Sick/S_75.jpg')
    evalImage_path = Path('/home/buybluepants/Documents/Thesis/Using-Large-Language-Models-to-identify-breast-cancer-cells/datasets/Breast Cancer Patients MRI\'s/validation/Healthy/S_75.jpg')
    resultFile_path = Path('/home/buybluepants/Documents/Thesis/Using-Large-Language-Models-to-identify-breast-cancer-cells/tempTests/GT0CompareS75_Sick_W_S75_Healthy.txt')
    test = encode_image_to_base64(baselineImage_path)
    models = get_model()
    process_directory(models, baselineImage_path, evalImage_path, resultFile_path)
    sort_model_entries(resultFile_path)
