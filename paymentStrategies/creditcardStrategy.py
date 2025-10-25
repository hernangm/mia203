import constants
import Payment

def validate(payment: Payment, payments: list):
    registered_payments_of_same_method = [
        p for p in payments
        if p.payment_method == payment.payment_method and p.status == constants.STATUS_REGISTRADO
    ]

    return payment.amount < 10000 and len(registered_payments_of_same_method) == 1