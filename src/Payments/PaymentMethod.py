from enum import Enum
from typing import Optional, Tuple

class PaymentMethod(str, Enum):
    PAYPAL = "PAYPAL"
    CREDIT_CARD = "CREDIT_CARD"

def parse_payment_method(raw: Optional[str]) -> PaymentMethod:
    """Case-insensitive, tolerant parsing for common variants (paypal, credit-card, credit_card)."""
    if raw is None:
        raise ValueError("payment method is None")
    norm = raw.strip().replace("-", "_").replace(" ", "_").upper()
    for pm in PaymentMethod:
        if norm == pm.value:
            return pm
    raise ValueError(f"invalid payment method: {raw!r}")

def try_get_payment_method(raw: Optional[str]) -> Tuple[bool, Optional[PaymentMethod]]:
    try:
        return True, parse_payment_method(raw)
    except ValueError:
        return False, None