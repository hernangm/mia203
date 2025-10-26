from typing import List
from ..payment import Payment
from ..payment_status import PaymentStatus
from .base_payment_method_validation_strategy import BasePaymentMethodValidationStrategy


class CreditCardValidationStrategy(BasePaymentMethodValidationStrategy):
    """
    Validation strategy for credit card payments.
    """
    def validate(self, payment: Payment, payments: List[Payment]) -> bool:
        """
        Validates that the payment amount is less than 10,000 and
        there is only one registered payment of the same method.
        """
        registered_payments_of_same_method = [
            p for p in payments
            if p.payment_method == payment.payment_method and p.status == PaymentStatus.REGISTRADO
        ]
        return payment.amount < 10000 and len(registered_payments_of_same_method) == 1