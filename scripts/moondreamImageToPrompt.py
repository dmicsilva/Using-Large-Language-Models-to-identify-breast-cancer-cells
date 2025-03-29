#pip install moondream==0.0.5

import moondream as md
from PIL import Image

# Initialize with local model path. Can also read .mf.gz files, but we recommend decompressing
# up-front to avoid decompression overhead every time the model is initialized.
model = md.vl(model="models/moondream-2b-int8.mf.gz")

# Load and process image
image = Image.open("data/image/360_F_252619416_B7LW83rSsQZyv3lO7y2hKL5fdS2bJp0L.webp")
encoded_image = model.encode_image(image)

# Generate caption
caption = model.caption(encoded_image)["caption"]
print("Caption:", caption)

# Ask questions
answer = model.query(encoded_image, "What's in this image?")["answer"]
print("Answer:", answer)