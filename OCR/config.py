# Configuration for OCR pipeline

# Tesseract settings
TESSERACT_LANGS = "eng+fas"
TESSERACT_DIR = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
PDF_DPI = 700

# Local Llama/Alpaca model for JSON extraction
USE_GGUF = True
MODEL_CP_TYPE = 'OPENAI'
LLAMA_MODEL_PATH = "C:\\Users\\Asus\\.lmstudio\\models\\lmstudio-community\\gpt-oss-20b-GGUF\\gpt-oss-20b-MXFP4.gguf"
GENERATION_CONFIG = {
    "temperature": 0.0,
    "top_p": 0.95,
    "max_new_tokens": 1024
}
