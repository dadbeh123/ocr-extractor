from celery import shared_task
from .pipelines import run_ocr_pipeline

@shared_task
def ocr_document_task(file_path: str):
    """
    Asynchronously process OCR + extraction.
    """
    inv = run_ocr_pipeline(file_path)
    return inv.id
