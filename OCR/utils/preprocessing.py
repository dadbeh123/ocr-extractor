import cv2
import numpy as np

def preprocess(image: np.ndarray) -> np.ndarray:
    """
    Grayscale → denoise → Otsu threshold.
    Input: H×W×3 BGR numpy array.
    Output: H×W binary numpy array.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, None, h=10)
    _, th = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th
