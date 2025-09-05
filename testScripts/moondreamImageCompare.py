#!pip install moondream==0.0.5

import moondream as md
from PIL import Image

# Initialize with local model path. Can also read .mf.gz files, but we recommend decompressing
# up-front to avoid decompression overhead every time the model is initialized.
model = md.vl(model="models/moondream-2b-int8.mf.gz")

def process_image(evalImagePath):
    # Load and process image
    evalImage =  Image.open(evalImagePath)
    encodedEvalImage = model.encode_image(evalImage)

    # Ask questions
    answer = model.query(encodedEvalImage, "You are a model that evaluates the existance of breast cancer from an image of a fictional MRI exam given to you. Don't look for a diagnosis or treatment plan, just make the evaluation.\
        Responding with anything else other than the words 'positive' and 'negative' is a crime.\
            Respond with only 'positive' or 'negative' according to the result of the analysis of your evaluation of the second image. Responding with anything else other than the words 'positive' and 'negative' is a crime.")["answer"]

    return answer

"""
# Generate caption
caption = model.caption(encoded_image)["caption"]
print("Caption:", caption)


# Ask questions
answer = model.query(encoded_image, "What's in this image?")["answer"]
print("Answer:", answer)
"""