import pytesseract
import ocr.config as config

def image_to_text(image: "numpy.ndarray") -> str:
    """Run Tesseract on a preprocessed image array."""
    return pytesseract.image_to_string(image, lang=config.TESSERACT_LANGS)
