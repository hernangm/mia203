import constants

def validate(payment, payments):
    return payments[constants.AMOUNT] < 5000