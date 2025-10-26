from typing import List
from ..payment import Payment
from .base_payment_method_validation_strategy import BasePaymentMethodValidationStrategy

class PayPalValidationStrategy(BasePaymentMethodValidationStrategy):
    """
    Validation strategy for PayPal payments.
    """
    def validate(self, payment: Payment, payments: List[Payment]) -> bool:
        """
        Validates that the payment amount is less than 5,000.
        """
        return payment.amount < 5000