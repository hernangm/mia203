
from typing import List
from Payment import Payment
from BasePaymentMethodValidationStrategy import BasePaymentMethodValidationStrategy

class PayPalValidationStrategy(BasePaymentMethodValidationStrategy):
    def validate(self, payment: Payment, payments: List[Payment]) -> bool:
        return payment.amount < 5000