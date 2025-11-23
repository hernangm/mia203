from payments.validation_strategies import CreditCardValidationStrategy
from payments.payment_status import PaymentStatus
from payments.payment_method import PaymentMethod

class MockPayment:
    def __init__(self, payment_id, amount, payment_method, status):
        self.payment_id = payment_id
        self.amount = amount
        self.payment_method = payment_method
        self.status = status

def test_validate_true_for_valid_payment():
    """
    Caso válido: monto < 10000 y existe exactamente 1 pago registrado previo.
    """
    strategy = CreditCardValidationStrategy()
    method = "CREDIT_CARD"
    payment = MockPayment("p1", 5000, method, PaymentStatus.REGISTRADO)
    payments = [
        MockPayment("p2", 100, method, PaymentStatus.REGISTRADO)
    ]
    assert strategy.validate(payment, payments)

def test_validate_false_for_high_amount():
    """
    Caso inválido: monto >= 10000
    """
    strategy = CreditCardValidationStrategy()
    method = "CREDIT_CARD"
    payment = MockPayment("p1", 15000, method, PaymentStatus.REGISTRADO)
    payments = [
        MockPayment("p2", 100, method, PaymentStatus.REGISTRADO)
    ]
    assert not strategy.validate(payment, payments)

def test_validate_false_for_no_registered_payments():
    """
    Caso inválido: no hay pagos registrados previos del mismo método
    """
    strategy = CreditCardValidationStrategy()
    method = "CREDIT_CARD"
    payment = MockPayment("p1", 5000, method, PaymentStatus.REGISTRADO)
    payments = []
    assert not strategy.validate(payment, payments)

def test_validate_false_for_multiple_registered_payments():    
    """
    Caso inválido: hay más de 1 pago registrado previo del mismo método
    """
    strategy = CreditCardValidationStrategy()
    method = "CREDIT_CARD"
    payment = MockPayment("p1", 5000, method, PaymentStatus.REGISTRADO)
    payments = [
        MockPayment("p2", 100, method, PaymentStatus.REGISTRADO),
        MockPayment("p3", 200, method, PaymentStatus.REGISTRADO)
    ]
    assert not strategy.validate(payment, payments)