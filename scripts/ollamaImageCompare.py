from pathlib import Path
import base64
import requests

endpoint = "http://localhost:11434/api/chat"
model = "llama3.2:1b"
#model = "deepseek-r1:1.5b"

def encode_image_to_base64(image_path):
    """Convert an image file to base64 string."""
    return base64.b64encode(image_path.read_bytes()).decode('utf-8')

def extract_knowledge_from_image(baselineImage_path, evalImage_path):
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
                    "You are a model that evaluates the existance of breast cancer from an image of a fictional MRI exam. Don't look for a diagnosis or treatment plan, just make the evaluation. \n"
                    "The first image you receive is your baseline, so consider it as a positive case. \n"
                    "The second image is the image you need to evaluate, according to the first image. \n"
                    "Respond with only 'positive' or 'negative' according to the result."
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

def process_directory():
    """Process all images in current directory and create text files."""
    baselineImage_path = Path('/home/buybluepants/Documents/Thesis/Using-Large-Language-Models-to-identify-breast-cancer-cells/datasets/Breast Cancer Patients MRI\'s/validation/Healthy/S_75.jpg')
    evalImage_path = Path('/home/buybluepants/Documents/Thesis/Using-Large-Language-Models-to-identify-breast-cancer-cells/datasets/Breast Cancer Patients MRI\'s/validation/Sick/S_75.jpg')

    print(f"\nProcessing {evalImage_path}...")

    text = extract_knowledge_from_image(baselineImage_path, evalImage_path)
    print(text)

process_directory()
