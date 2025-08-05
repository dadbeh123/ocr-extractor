import json
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    GenerationConfig
)
from .normalizer import normalize_text
from .validator import validate_and_format_llm
from .integration import save_to_db
import ocr.config as config

# Load tokenizer & model once
tokenizer = AutoTokenizer.from_pretrained(
    config.LLAMA_MODEL_PATH, use_fast=False
)
model = AutoModelForCausalLM.from_pretrained(
    config.LLAMA_MODEL_PATH,
    device_map="auto",
    torch_dtype=torch.float16,
    trust_remote_code=True
)
gen_cfg = GenerationConfig(**config.GENERATION_CONFIG, 
                           eos_token_id=tokenizer.eos_token_id)

def extract_with_llm(ocr_text: str) -> dict:
    prompt = (
        "You are a JSON extractor for multi-lingual invoices (English & Persian).\n"
        "Extract exactly the following fields and output only a single JSON object:\n"
        "- vendor: string\n"
        "- date: string (YYYY-MM-DD)\n"
        "- total: number\n"
        "- line_items: array of objects, each with:\n"
        "    - description: string\n"
        "    - quantity: number\n"
        "    - unit_price: number\n"
        "    - line_total: number\n\n"
        "Here is the raw OCR text (already normalized):\n"
        "----------------------------------------\n"
        f"{ocr_text}\n"
        "----------------------------------------\n"
    )
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True).to(model.device)
    outputs = model.generate(**inputs, generation_config=gen_cfg)
    raw = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # strip everything before first JSON brace
    json_str = raw[raw.find("{"):]
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON from LLM:\n{json_str}") from e

def extract_fields_with_llm(raw_text: str, source_file: str):
    norm = normalize_text(raw_text)
    data = extract_with_llm(norm)
    validated = validate_and_format_llm(data)
    return save_to_db(validated, source_file)
