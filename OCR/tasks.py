import argparse
from celery import shared_task
from .pipelines import run_ocr_pipeline

# @shared_task
def ocr_document_task(file_path: str):
    """
    Asynchronously process OCR + extraction.
    """
    inv = run_ocr_pipeline(file_path)
    return inv

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run OCR pipeline")
    parser.add_argument("-f", "--file", type=str, help="Path to the document file", required=True)

    args = parser.parse_args()

    # print(ocr_document_task.apply_async((args.file,), countdown=0))
    print(ocr_document_task(args.file))
