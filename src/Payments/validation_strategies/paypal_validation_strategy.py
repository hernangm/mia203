from typing import List
from payments import Payment
from payments.validation_strategies import BasePaymentMethodValidationStrategy

class PayPalValidationStrategy(BasePaymentMethodValidationStrategy):
    """
    Validation strategy for PayPal payments.
    """
    def validate(self, payment: Payment, payments: List[Payment]) -> bool:
        """
        Validates that the payment amount is less than 5,000.
        """
        return payment.amount < 5000