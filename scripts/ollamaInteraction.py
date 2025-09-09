from pathlib import Path
import base64
import requests
import parameters
import fileInteraction as fi

def extract_knowledge_from_image(evalImage_path, model, prompt):

    evalImage_base64 = fi.encode_image_to_base64(evalImage_path)

    payload = {
        "model": model,
        "stream": False,
        "messages": [
            {
                "role": "user",
                "content": prompt,
                "images": [evalImage_base64]
            }
        ]
    }

    response = requests.post(
        parameters.endpoint,
        json=payload,
        headers={"Content-Type": "application/json"}
    )

    return response.json().get('message', {}).get('content', 'No text extracted')


def get_model():

    try:
        localGetModelResponse = requests.get(parameters.getModelEndpoint)

        if localGetModelResponse.status_code == 200:
            models = localGetModelResponse.json()["models"]
            
            print("\n\nAvailable models:\n")
            for i, localModel in enumerate(models):
                print(f"{i+1}. {localModel['name']}")
            print("a. All")

            modelNameList = [model['name'] for model in models]
            choice = input("\nChoose a model: ")
            
            if choice.lower() == 'a':
                return modelNameList
            elif 1 <= int(choice) <= len(modelNameList):
                localModel = [models[int(choice) - 1]["name"]]
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