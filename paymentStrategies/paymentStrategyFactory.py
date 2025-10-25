from paymentStrategies.paypalStrategy import validate as paypal_validate
from paymentStrategies.creditcardStrategy import validate as creditcard_validate

def get(payment_method: str):
    if payment_method == "PAYPAL":
        return paypal_validate
    elif payment_method == "CREDITARD":
        return creditcard_validate
    else:
        return None