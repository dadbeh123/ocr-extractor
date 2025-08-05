import re
import spacy
import ocr.config as config

# Fallback Regex + spaCy NER (if you choose to use it)
nlp_en = spacy.load(config.ML_MODEL["english"])

DATE_REGEX = re.compile(r"\b(\d{4}/\d{2}/\d{2}|\d{2}-\d{2}-\d{4}|"
                        r"\d{2}\s+[A-Za-z]{3,}\s+\d{4})\b")
TOTAL_REGEX = re.compile(r"\b(?:Total|Amount Due|مبلغ\s*کل)[:\s\-]*([\d\.,]+)\b",
                         flags=re.IGNORECASE)

def extract_fields(text: str) -> dict:
    data = {}

    # Regex-based
    m = DATE_REGEX.search(text)
    if m:
        data["date"] = m.group(1)
    m = TOTAL_REGEX.search(text)
    if m:
        data["total"] = m.group(1)

    # spaCy NER fallback
    doc = nlp_en(text)
    for ent in doc.ents:
        if ent.label_ in ("ORG","PERSON") and "vendor" not in data:
            data["vendor"] = ent.text

    return data
