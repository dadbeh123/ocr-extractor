import numpy as np
from .utils.ingestion import load_images
from .utils.preprocessing import preprocess
from .utils.ocr_engine import image_to_text
from .utils.llm_extractor import extract_fields_with_llm

def run_ocr_pipeline(file_path: str):
    """
    Full end-to-end OCR → LLM extraction → validation → save.
    """
    # 1) Ingest PDF/image → PIL Images
    images = load_images(file_path)

    # 2) OCR all pages
    full_text = ""
    for img in images:
        arr = np.array(img.convert("RGB"))
        bin_img = preprocess(arr)
        raw = image_to_text(bin_img)
        full_text += raw + "\n"

    # 3) LLM extraction + save to DB
    invoice = extract_fields_with_llm(full_text, file_path)
    return invoice
