from enum import Enum
from typing import Optional, Tuple

class PaymentStatus(str, Enum):
    """
    Enum representing possible payment statuses.
    """
    REGISTRADO = "REGISTRADO"
    PAGADO = "PAGADO"
    FALLIDO = "FALLIDO"

def parse_payment_status(raw: Optional[str]) -> PaymentStatus:
    """
    Returns the PaymentStatus if the string matches exactly one of the enum values (after strip).
    Raises ValueError if the string is null, empty, or does not match any enum value.
    """
    if raw is None:
        raise ValueError("payment status is None")
    key = raw.strip()
    if not key:
        raise ValueError("payment status is empty")
    for ps in PaymentStatus:
        if key == ps.value:
            return ps
    raise ValueError(f"invalid payment status: {raw!r}")

def try_get_payment_status(raw: Optional[str]) -> Tuple[bool, Optional[PaymentStatus]]:
    """
    Wraps parse_payment_status: returns (True, PaymentStatus) if parsing succeeded,
    or (False, None) if it failed (does not propagate the exception).
    """
    try:
        ps = parse_payment_status(raw)
        return True, ps
    except ValueError:
        return False, None