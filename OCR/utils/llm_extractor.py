import json
import torch
import ocr.config as config
from .normalizer import normalize_text
from .validator import validate_and_format_llm

if not config.USE_GGUF:
    from transformers import (
        AutoTokenizer,
        AutoModelForCausalLM,
        GenerationConfig
    )

    # Load tokenizer & model (Hugging Face Transformers)
    tokenizer = AutoTokenizer.from_pretrained(
        config.LLAMA_MODEL_PATH, use_fast=False
    )
    model = AutoModelForCausalLM.from_pretrained(
        config.LLAMA_MODEL_PATH,
        device_map="auto",
        torch_dtype=torch.float16,
        trust_remote_code=True
    )
    gen_cfg = GenerationConfig(
        **config.GENERATION_CONFIG,
        eos_token_id=tokenizer.eos_token_id
    )

elif config.MODEL_CP_TYPE == 'OPENAI':
    from openai import OpenAI

    client = OpenAI(
        base_url="http://localhost:1234/v1",
        api_key="lm-studio"
    )

else:
    from llama_cpp import Llama

    # Load GGUF model using llama-cpp-python
    model = Llama(
        model_path=config.LLAMA_MODEL_PATH,  # This should point to a .gguf file
        n_gpu_layers=-1,                     # Use GPU if available, -1 for all layers
        n_ctx=10000,
        f16_kv=True,
        verbose=False
    )

def build_prompt(ocr_text: str) -> str:
    return (
        "You are a JSON extractor for multi-lingual invoices (English & Persian).\n"
        "Extract exactly the following fields and output only a single JSON object. If there is not a value for a field then put a default value for it:\n"
        "- vendor: string\n"
        "- date: string (YYYY-MM-DD)\n"
        "- total: number\n"
        "- line_items: array of objects, each with:\n"
        "    - description: string\n"
        "    - quantity: number\n"
        "    - unit_price: number\n"
        "    - line_total: number\n\n"
        "Here is the raw OCR text (already normalized):\n"
        f"{ocr_text}\n"
        "OUTPUT ONLY THE JSON OBJECT WITH NOTHING ELSE. DO NOT REPEAT THE SEPARATORS.\n"
    )

def extract_with_llm(ocr_text: str) -> dict:
    prompt = build_prompt(ocr_text)

    if config.USE_GGUF:
        if config.MODEL_CP_TYPE == 'OPENAI':
            response = client.chat.completions.create(
            model="gpt-oss:20b",
            messages=[
                        {"role": "system", "content": prompt},
                     ]
            )
            raw = response.choices[0].message.content
        else:
            response = model(
                            prompt,
                            max_tokens=config.GENERATION_CONFIG["max_new_tokens"],
                            stop=["<|eot_id|>", "\n\n", "\n"],
                            echo=False,
                            temperature=config.GENERATION_CONFIG["temperature"]
                            )
            raw = response["choices"][0]["text"]
    else:
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True).to(model.device)
        outputs = model.generate(**inputs, generation_config=gen_cfg)
        raw = tokenizer.decode(outputs[0], skip_special_tokens=True)

    json_str = raw[raw.find("{"):]
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON from LLM:\n{json_str}") from e

def extract_fields_with_llm(raw_text: str):
    norm = normalize_text(raw_text)
    data = extract_with_llm(norm)
    validated = validate_and_format_llm(data)
    return validated
