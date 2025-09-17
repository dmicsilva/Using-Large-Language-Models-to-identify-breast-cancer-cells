import parameters
from unsloth import FastLanguageModel
import torch
from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments
from unsloth import is_bfloat16_supported
import sys

def load_model_tokenizer(modelName):
    
    max_seq_length = 2048 # Choose any! We auto support RoPE Scaling internally!
    dtype = None # None for auto detection. Float16 for Tesla T4, V100, Bfloat16 for Ampere+
    load_in_4bit = True # Use 4bit quantization to reduce memory usage. Can be False.

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name = modelName,
        max_seq_length = max_seq_length,
        dtype = dtype,
        load_in_4bit = load_in_4bit,
        # token = "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"
    )

    model = FastLanguageModel.get_peft_model(
        model,
        r = 16, # Choose any number > 0 ! Suggested 8, 16, 32, 64, 128
        target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj",],
        lora_alpha = 16,
        lora_dropout = 0, # Supports any, but = 0 is optimized
        bias = "none",    # Supports any, but = "none" is optimized
        # [NEW] "unsloth" uses 30% less VRAM, fits 2x larger batch sizes!
        use_gradient_checkpointing = "unsloth", # True or "unsloth" for very long context
        random_state = 3407,
        use_rslora = False,  # We support rank stabilized LoRA
        loftq_config = None, # And LoftQ
    )

    return model, tokenizer


def prepare_dataset(datasetName):

    selectedDataset = get_dataset(datasetName)
    dataset = load_dataset(selectedDataset['hugginFace'])

    selectedInstruction = get_instruction(datasetName)
    instruction = selectedInstruction['instruction']

    dataset = dataset["train"].map(
        lambda row: format_chat_template(row, instruction),
        num_proc= 4,
    )
    dataset["text"][2]

    if selectedDataset['splitTrain']:
        dataset = dataset.train_test_split(test_size=0.1)

    return dataset


def format_chat_template(row, instruction):
    
    row_json = [{"role": "system", "content": instruction },
               {"role": "user", "content": row["base64_encoded_image"]},
               {"role": "assistant", "content": row["cancerExistance"]}]
    
    row["text"] = tokenizer.apply_chat_template(row_json, tokenize=False, add_generation_prompt=False, return_tensors="pt")
    return row


def initiate_trainer(model, tokenizer, dataset, fineTunedModelName):

    max_seq_length = 2048 # Choose any! We auto support RoPE Scaling internally!

    trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset,
    dataset_text_field = "text",
    max_seq_length = max_seq_length,
    dataset_num_proc = 2,
    packing = False, # Can make training 5x faster for short sequences.
    args = TrainingArguments(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        warmup_steps = 5,
        # num_train_epochs = 1, # Set this for 1 full training run.
        max_steps = 60,
        learning_rate = 2e-4,
        fp16 = not is_bfloat16_supported(),
        bf16 = is_bfloat16_supported(),
        logging_steps = 1,
        optim = "adamw_8bit",
        weight_decay = 0.01,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "outputs",
        ),
    )

    # Start Fine-tuning job
    trainer_stats = trainer.train()
    
    # Save the model
    """<a name="Save"></a>
    ### Saving, loading finetuned models
    To save the final model as LoRA adapters, either use Huggingface's `push_to_hub` for an online save or `save_pretrained` for a local save.
    """
    model.save_pretrained(f"{fineTunedModelName}") # Local saving
    tokenizer.save_pretrained(f"{fineTunedModelName}")
    
    # Save to 8bit Q8_0
    if True: model.save_pretrained_gguf("model", tokenizer, quantization_method = [ "q8_0"])

    return


def get_dataset(datasetName):

    try:
        for dataset in parameters.datasets:
            if dataset['label'] == datasetName:
                selectedDataset = dataset
        return selectedDataset

    except:
        print("No dataset corresponding name.")
        return

def get_instruction(datasetName):

    try:
        for instruction in parameters.instructions:
            if instruction['label'] == datasetName:
                selectedInstruction = instruction
        return selectedInstruction
    
    except:
        print("No instruction defined for the dataset.")
        return


def choose_dataset(): #redo datatypes

    print("Choose a dataset")
    for i, dataset in enumerate(parameters.datasets):
        print(f"{i+1}. {dataset['label']}")

    while True:
        choice = input("Enter the number of your chosen dataset (or 'q' to quit): ")
        
        if choice.lower() == "q":
            sys.exit()

        try:
            choice = int(choice)
            if 1 <= choice <= len(parameters.datasets):
                return parameters.datasets[choice-1]['label']
            else:
                print("Invalid choice. Please choose a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q' to quit.")

    return


def choose_model():

    print("Choose a model")
    for i, model in enumerate(parameters.models):
        print(f"{i+1}. {model}")

    while True:
        choice = input("Enter the number of your chosen model (or 'q' to quit): ")
        
        if choice.lower() == "q":
            sys.exit()

        try:
            choice = int(choice)
            if 1 <= choice <= len(parameters.models):
                return parameters.models[choice-1]
            else:
                print("Invalid choice. Please choose a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q' to quit.")

    return


if __name__ == "__main__":

    modelName = choose_model()
    datasetName = choose_dataset()
    simpleModelName = modelName.split("/")[1]
    fineTunedModelName = f"{datasetName}Finetuned_{simpleModelName}"

    model, tokenizer = load_model_tokenizer(modelName)
    dataset = prepare_dataset(datasetName)

    initiate_trainer(model, tokenizer, dataset, fineTunedModelName)