from pathlib import Path
import glob
import subprocess

LLAVA_EXEC_PATH = "llama.cpp/build/bin/llama-llava-cli"
MODEL_PATH = "models/ggml-model-q4_k.gguf"
MMPROJ_PATH = "models/mmproj-model-f16.gguf"

DATA_DIR = "data"
IMAGE_DIR = Path(DATA_DIR, "image")
TXT_DIR = Path(DATA_DIR, "txt")

image_paths = sorted(glob.glob(str(IMAGE_DIR.joinpath("*.jpg"))))

TEMP = 0.1
PROMPT = "The image shows a site in Paris. Describe the image like a tourist guide would."

bash_command = f'{LLAVA_EXEC_PATH} -m {MODEL_PATH} --mmproj {MMPROJ_PATH} --temp {TEMP} -p "{PROMPT}"'

for image_path in image_paths:
    print(f"Processing {image_path}")
    image_name = Path(image_path).stem
    image_summary_path = TXT_DIR.joinpath(image_name + ".txt")

    # add input image and output txt filenames to bash command
    bash_command_cur = f'{bash_command} --image "{image_path}" > "{image_summary_path}"'

    # run the bash command
    process = subprocess.Popen(
        bash_command_cur, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    # get the output and error from the command
    output, error = process.communicate()

    # commment output and error for less verbose output
    print("Output:")
    print(output.decode("utf-8"))

    print("Error:")
    print(error.decode("utf-8"))

    # return the code of the command 
    return_code = process.returncode
    print(f"Return code: {return_code}")
    print()

print("Done")

image_texts = []

for filepath in image_paths:
    with open(filepath, "r") as f:
        image_text = f.read()
    image_texts.append(image_text)

image_text_cleaned = []

for text_index, image_text in enumerate(image_texts):
    # split the text by new lines
    image_text_split = image_text.split("\n")

    # find index of the line that starts with prompt:
    start_index_list = [
        i for i, line in enumerate(image_text_split) if line.startswith("prompt:")
    ]

    # find index of the line that starts with main:
    end_index_list = [
        i for i, line in enumerate(image_text_split) if line.startswith("main:")
    ]

    if (
        len(start_index_list) != 1
        or len(end_index_list) != 1
        or start_index_list[0] < start_index_list[0]
    ):
        # there was a problem with image text
        print(f"Warning: start/end indices couldn''t be found for document {text_index}")
        continue

    start_index = start_index_list[0]
    end_index = end_index_list[0]

    # extract the text based on indices above
    image_text_cleaned.append(
        "".join(image_text_split[start_index + 1 : end_index]).strip()
    )

for text in image_text_cleaned:
    print(text)
