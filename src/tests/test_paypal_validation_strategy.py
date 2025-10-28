from payments.validation_strategies import PayPalValidationStrategy

class MockPayment:
    def __init__(self, amount):
        self.amount = amount

def test_validate_returns_true_for_amount_below_limit():
    """
    Test that PayPalValidationStrategy returns True when the payment amount is below 5000.
    """
    strategy = PayPalValidationStrategy()
    payment = MockPayment(4999.99)
    payments = []
    assert strategy.validate(payment, payments)

def test_validate_returns_false_for_amount_equal_limit():
    """
    Test that PayPalValidationStrategy returns False when the payment amount is exactly 5000.
    """
    strategy = PayPalValidationStrategy()
    payment = MockPayment(5000)
    payments = []
    assert not strategy.validate(payment, payments)

def test_validate_returns_false_for_amount_above_limit():
    """
    Test that PayPalValidationStrategy returns False when the payment amount is above 5000.
    """
    strategy = PayPalValidationStrategy()
    payment = MockPayment(6000)
    payments = []
    assert not strategy.validate(payment, payments)