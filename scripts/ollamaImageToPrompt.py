from pathlib import Path
import base64
import requests

endpoint = "http://localhost:11434/api/chat"
#model = "moondream"
#model = "llama3.2:1b"
model = "deepseek-r1:1.5b"

def encode_image_to_base64(image_path):
    """Convert an image file to base64 string."""
    return base64.b64encode(image_path.read_bytes()).decode('utf-8')

def extract_knowledge_from_image(image_path):
    """Send image to local Llama API and get text description."""
    base64_image = encode_image_to_base64(image_path)

    payload = {
        "model": model,
        "stream": False,
        "messages": [
            {
                "role": "user",
                "content": (
                    "This is an image of Paris \n"
                    "Provide a comprehensive description of the image, focusing on key elements such as subjects, \
                        objects, setting, and any notable details and visual style. Describe the style of the image (e.g., realistic, abstract, vintage) \
                            and the atmosphere it conveys. Merge all information into a seamless paragraph without using the ‘What, Who, Where, When, How’ structure. \
                                Provide the ratio and orientation after the description. "
                ),
                "images": [base64_image]
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
    textFolderDirectory = Path('data/txt')
    for image_path in Path('data/image').glob('*'):
        if image_path.suffix.lower() in {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}:
            print(f"\nProcessing {image_path}...")

            text = extract_knowledge_from_image(image_path)
            textFolderDirectory.with_stem(model).with_suffix('.txt').write_text(text, encoding='utf-8')
            print(f"Created {image_path.with_suffix('.txt')}")

process_directory()
