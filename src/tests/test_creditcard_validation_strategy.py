import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import Payments.PaymentMethod as pm_mod
pm_mod.PaymentMethod.REGISTRADO = "REGISTRADO"

from Payments.PaymentValidationStrategies.CreditCardValidationStrategy import CreditCardValidationStrategy

class MockPaymentMethod:
    REGISTRADO = "REGISTRADO"

class MockPayment:
    def __init__(self, payment_id, amount, payment_method, status):
        self.payment_id = payment_id
        self.amount = amount
        self.payment_method = payment_method
        self.status = status

def test_validate_true_for_valid_payment():
    strategy = CreditCardValidationStrategy()
    method = MockPaymentMethod()
    payment = MockPayment("p1", 5000, method, method.REGISTRADO)
    payments = [
        MockPayment("p2", 100, method, method.REGISTRADO)
    ]
    assert strategy.validate(payment, payments) is True

def test_validate_false_for_high_amount():
    strategy = CreditCardValidationStrategy()
    method = MockPaymentMethod()
    payment = MockPayment("p1", 15000, method, method.REGISTRADO)
    payments = [
        MockPayment("p2", 100, method, method.REGISTRADO)
    ]
    assert strategy.validate(payment, payments) is False

def test_validate_false_for_no_registered_payments():
    strategy = CreditCardValidationStrategy()
    method = MockPaymentMethod()
    payment = MockPayment("p1", 5000, method, method.REGISTRADO)
    payments = []
    assert strategy.validate(payment, payments) is False

def test_validate_false_for_multiple_registered_payments():
    strategy = CreditCardValidationStrategy()
    method = MockPaymentMethod()
    payment = MockPayment("p1", 5000, method, method.REGISTRADO)
    payments = [
        MockPayment("p2", 100, method, method.REGISTRADO),
        MockPayment("p3", 200, method, method.REGISTRADO)
    ]
    assert strategy.validate(payment, payments) is False