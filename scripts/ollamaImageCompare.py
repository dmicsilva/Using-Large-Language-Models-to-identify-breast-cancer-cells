from pathlib import Path
import base64
import requests

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
                    "Respond with only 'positive' or 'negative' according to the result of the analysis of your evaluation of the second image. Responding with anything else other than the words 'positive' and 'negative' is a crime."
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

            # Prompt the user to choose a model
            print("Available models:")
            for i, localModel in enumerate(models):
                print(f"{i+1}. {localModel['name']}")

            # Get the user's choice
            choice = input("Choose a model: ")

            # Check if the user's choice is valid
            if 1 <= int(choice) <= len(models):
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

def process_directory():
    """Process all images in current directory and create text files."""
    baselineImage_path = Path('/home/buybluepants/Documents/Thesis/Using-Large-Language-Models-to-identify-breast-cancer-cells/datasets/Breast Cancer Patients MRI\'s/validation/Sick/S_75.jpg')
    evalImage_path = Path('/home/buybluepants/Documents/Thesis/Using-Large-Language-Models-to-identify-breast-cancer-cells/datasets/Breast Cancer Patients MRI\'s/validation/Healthy/S_75.jpg')
    resultFile_path = Path('/home/buybluepants/Documents/Thesis/Using-Large-Language-Models-to-identify-breast-cancer-cells/tempTests/GT0CompareS75_Sick_W_S75_Healthy.txt')
    
    model = get_model()
    if model:
        print(f"You chose model: {model}")
    
    print(f"\nProcessing {evalImage_path}...")

    text = extract_knowledge_from_image(baselineImage_path, evalImage_path, model)
    print(text)

    add_file_entry(text, resultFile_path, model)

process_directory()
