import Payment

def validate(payment: Payment, payments: list):
    return payment.amount < 5000