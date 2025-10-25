from enum import Enum
from typing import Optional, Tuple

class PaymentStatus(str, Enum):
    REGISTRADO = "REGISTRADO"
    PAGADO = "PAGADO"
    FALLIDO = "FALLIDO"

def parse_payment_status(raw: Optional[str]) -> PaymentStatus:
    """
    Devuelve el PaymentStatus si la cadena coincide exactamente con uno de los valores del enum (tras strip).
    Lanza ValueError si la cadena es nula, vacía o no coincide con ningún valor del enum.
    """
    if raw is None:
        raise ValueError("payment method is None")
    key = raw.strip()
    if not key:
        raise ValueError("payment method is empty")
    for pm in PaymentStatus:
        if key == pm.value:
            return pm
    raise ValueError(f"invalid payment method: {raw!r}")

def try_get_payment_status(raw: Optional[str]) -> Tuple[bool, Optional[PaymentStatus]]:
    """
    Envuelve parse_payment_method: devuelve (True, PaymentStatus) si el parseo tuvo éxito,
    o (False, None) si falló (no propaga la excepción).
    """
    try:
        pm = parse_payment_status(raw)
        return True, pm
    except ValueError:
        return False, None