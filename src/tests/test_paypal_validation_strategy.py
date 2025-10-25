import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Payments.PaymentValidationStrategies.PayPalValidationStrategy import PayPalValidationStrategy

class MockPayment:
    def __init__(self, amount):
        self.amount = amount

def test_validate_returns_true_for_amount_below_limit():
    strategy = PayPalValidationStrategy()
    payment = MockPayment(4999.99)
    payments = []
    assert strategy.validate(payment, payments) is True

def test_validate_returns_false_for_amount_equal_limit():
    strategy = PayPalValidationStrategy()
    payment = MockPayment(5000)
    payments = []
    assert strategy.validate(payment, payments) is False

def test_validate_returns_false_for_amount_above_limit():
    strategy = PayPalValidationStrategy()
    payment = MockPayment(6000)
    payments = []
    assert strategy.validate(payment, payments) is False