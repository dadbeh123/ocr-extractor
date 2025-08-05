from datetime import datetime
from decimal import Decimal

def validate_and_format_llm(extracted: dict) -> dict:
    """
    Convert date→dateobj, numeric strings→Decimal/float,
    verify sum(line_items)==total.
    """
    # Date
    dt = datetime.strptime(extracted["date"], "%Y-%m-%d")
    extracted["date"] = dt.date()

    # Numbers
    extracted["total"] = Decimal(str(extracted["total"]))
    for item in extracted.get("line_items", []):
        item["quantity"]   = Decimal(str(item["quantity"]))
        item["unit_price"] = Decimal(str(item["unit_price"]))
        item["line_total"] = Decimal(str(item["line_total"]))

    # Consistency check
    sum_items = sum(i["line_total"] for i in extracted["line_items"])
    if abs(sum_items - extracted["total"]) > Decimal("0.01"):
        raise ValueError("Line‐item sum does not match total.")

    return extracted
