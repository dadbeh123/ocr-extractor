# Configuration for OCR pipeline

# Tesseract settings
TESSERACT_LANGS = "eng+fas"
PDF_DPI = 300

# (Unused here but left for regex/NER fallback)
ML_MODEL = {
    "english": "en_core_web_sm",
    "persian": "/path/to/your/parsbert-ner",
    "layout": "impira/layoutlm-document-qa"
}

# Local Llama/Alpaca model for JSON extraction
LLAMA_MODEL_PATH = "/path/to/your/llama-model"
GENERATION_CONFIG = {
    "temperature": 0.0,
    "top_p": 0.95,
    "max_new_tokens": 512
}
