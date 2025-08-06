# Configuration for OCR pipeline

# Tesseract settings
TESSERACT_LANGS = "eng+fas"
TESSERACT_DIR = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
PDF_DPI = 700

# Local Llama/Alpaca model for JSON extraction
USE_GGUF = True
LLAMA_MODEL_PATH = "C:\\Users\\Asus\\.lmstudio\\models\\lmstudio-community\\Meta-Llama-3.1-8B-Instruct-GGUF\\Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
GENERATION_CONFIG = {
    "temperature": 0.0,
    "top_p": 0.95,
    "max_new_tokens": 1024
}
