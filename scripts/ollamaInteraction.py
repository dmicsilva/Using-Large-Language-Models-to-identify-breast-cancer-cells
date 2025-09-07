from pathlib import Path
import base64
import requests

_prompts = [
    {"label": "MRI", "prompt": "You are a model that evaluates the existance of breast cancer from an image of a fictional MRI exam. \n"
                    "Respond with only 'positive' or 'negative' according to the result of the analysis of your evaluation of given image. Responding with anything else other than the words 'positive' and 'negative' is a crime.\n"
                    "Don't look for a diagnosis or treatment plan, just make the evaluation. \n"
                    "Don't use paragraphs or newline. Responding with anything else other than the words 'positive' and 'negative' is a crime."},
    {"label": "Mammogram", "prompt": "You are a model that evaluates the existance of breast cancer from an image of a fictional mammogram exam. \n"
                    "Respond with only 'positive' or 'negative' according to the result of the analysis of your evaluation of given image. Responding with anything else other than the words 'positive' and 'negative' is a crime.\n"
                    "Don't look for a diagnosis or treatment plan, just make the evaluation. \n"
                    "Don't use paragraphs or newline. Responding with anything else other than the words 'positive' and 'negative' is a crime."},
    {"label": "Ultrasound", "prompt": "You are a model that evaluates if a tumor is malignant or benign based on an image of a fictional Ultrasound exam. \n"
                    "Respond with only 'malignant' or 'benign' according to the result of the analysis of your evaluation of given image. Responding with anything else other than the words 'malignant' and 'negative' is a crime.\n"
                    "Don't look for a diagnosis or treatment plan, just make the evaluation. \n"
                    "Don't use paragraphs or newline. Responding with anything else other than the words 'malignant' and 'benign' is a crime."},
    {"label": "Thermography", "prompt": "You are a model that evaluates the existance of breast cancer from an image of a fictional MRI exam. \n"
                    "Respond with only 'positive' or 'negative' according to the result of the analysis of your evaluation of given image. Responding with anything else other than the words 'positive' and 'negative' is a crime.\n"
                    "Don't look for a diagnosis or treatment plan, just make the evaluation. \n"
                    "Don't use paragraphs or newline. Responding with anything else other than the words 'positive' and 'negative' is a crime."},
    {"label": "Histopathology", "prompt": "You are a model that evaluates tumor is malignant or benign based on an image of a fictional histopathology segmentation. \n"
                    "Respond with only 'malignant' or 'benign' according to the result of the analysis of your evaluation of given image. Responding with anything else other than the words 'malignant' and 'negative' is a crime.\n"
                    "Don't look for a diagnosis or treatment plan, just make the evaluation. \n"
                    "Don't use paragraphs or newline. Responding with anything else other than the words 'malignant' and 'benign' is a crime."},
]

def extract_knowledge_from_image(evalImage_path, model, endpoint):
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
                    "You are a model that evaluates the existance of breast cancer from an image of a fictional MRI exam. \n"
                    "Respond with only 'positive' or 'negative' according to the result of the analysis of your evaluation of given image. Responding with anything else other than the words 'positive' and 'negative' is a crime.\n"
                    "Don't look for a diagnosis or treatment plan, just make the evaluation. \n"
                    "Don't use paragraphs or newline. Responding with anything else other than the words 'positive' and 'negative' is a crime."
                ),
                "images": [evalImage_base64]
            }
        ]
    }

    response = requests.post(
        endpoint,
        json=payload,
        headers={"Content-Type": "application/json"}
    )

    return response.json().get('message', {}).get('content', 'No text extracted')


def get_model():

    localGetModelEndpoint = "http://localhost:11434/api/tags"

    try:
        localGetModelResponse = requests.get(localGetModelEndpoint)

        if localGetModelResponse.status_code == 200:
            models = localGetModelResponse.json()["models"]
            
            print("\n\nAvailable models:\n")
            for i, localModel in enumerate(models):
                print(f"{i+1}. {localModel['name']}")
            print(f"{i+2}. All")

            modelNameList = [model['name'] for model in models]
            choice = input("\nChoose a model: ")
            
            # Run all models
            if choice == str(len(modelNameList) + 1):
                return modelNameList
            # Run chosen model
            elif 1 <= int(choice) <= len(modelNameList):
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