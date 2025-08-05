from pdf2image import convert_from_path
from PIL import Image
import ocr.config as config

def load_images(file_path: str) -> list[Image.Image]:
    """Load JPEG/PNG or multi-page PDF into a list of PIL Images."""
    if file_path.lower().endswith(".pdf"):
        return convert_from_path(file_path, dpi=config.PDF_DPI)
    else:
        return [Image.open(file_path)]
