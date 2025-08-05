import re

# Map Persian digits + punctuation → Western
PERSIAN_NUM_MAP = str.maketrans("۰۱۲۳۴۵۶۷۸۹٬", "0123456789,")

def normalize_text(raw: str) -> str:
    txt = raw.translate(PERSIAN_NUM_MAP)
    txt = re.sub(r"[ \t]+", " ", txt)
    txt = re.sub(r"\r\n?", "\n", txt)
    return txt.strip()
