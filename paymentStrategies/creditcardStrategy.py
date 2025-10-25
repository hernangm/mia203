import constants

def validate(payment, payments):
    pagos_registrados = [
        p for p in payments
        if p[constants.PAYMENT_METHOD] == payment[constants.PAYMENT_METHOD] and p[constants.STATUS] == constants.STATUS_REGISTRADO
    ]

    return payment[constants.AMOUNT] < 10000 and len(pagos_registrados) == 1