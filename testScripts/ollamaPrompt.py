import requests

endpoint = "http://localhost:11434/api/chat"
#model = "deepseek-r1:1.5b"
model = "llama3.2:1b"

def send_text_prompt(prompt):
    payload = {
        "model": model,
        "stream": False,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(endpoint, json=payload, headers={"Content-Type": "application/json"})
    return response.json().get('message', {}).get('content', 'No response received')

prompt = "Tell me a joke"
response = send_text_prompt(prompt)
print("Model Response:", response)
