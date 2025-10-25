from paymentStrategies.paypalStrategy import validate as paypal_validate
from paymentStrategies.creditcardStrategy import validate as creditcard_validate

def get(payment_method: str):
    normalized_method = payment_method.upper()
    if normalized_method == "PAYPAL":
        return paypal_validate
    elif normalized_method == "CREDIT_CARD": # Corrected typo and case-insensitivity
        return creditcard_validate
    else:
        return None