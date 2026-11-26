"""LoRA fine-tune on qa.jsonl from `fivesenses dataset`. Needs a GPU: pip install unsloth trl datasets.
Untested here (no GPU in the build environment); treat as a starting point."""
import sys
from datasets import load_dataset
from unsloth import FastLanguageModel
from trl import SFTTrainer, SFTConfig

data = sys.argv[1] if len(sys.argv) > 1 else "qa.jsonl"
base = sys.argv[2] if len(sys.argv) > 2 else "unsloth/Qwen2.5-7B-Instruct-bnb-4bit"
model, tok = FastLanguageModel.from_pretrained(base, max_seq_length=2048, load_in_4bit=True)
model = FastLanguageModel.get_peft_model(model, r=16, lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"])
ds = load_dataset("json", data_files=data, split="train")
ds = ds.map(lambda r: {"text": tok.apply_chat_template(r["messages"], tokenize=False)})
SFTTrainer(model=model, train_dataset=ds, tokenizer=tok,
    args=SFTConfig(output_dir="lora-out", per_device_train_batch_size=2, gradient_accumulation_steps=4,
                   num_train_epochs=2, learning_rate=2e-4, logging_steps=10, dataset_text_field="text")).train()
model.save_pretrained("lora-out")
