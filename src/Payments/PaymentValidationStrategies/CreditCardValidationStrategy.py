from typing import List
from Payments.Payment import Payment
from Payments.PaymentMethod import PaymentMethod
from .BasePaymentMethodValidationStrategy import BasePaymentMethodValidationStrategy


class CreditCardValidationStrategy(BasePaymentMethodValidationStrategy):
    def validate(self, payment: Payment, payments: List[Payment]) -> bool:
        registered_payments_of_same_method = [
            p for p in payments
            if p.payment_method == payment.payment_method and p.status == PaymentMethod.REGISTRADO
        ]
        return payment.amount < 10000 and len(registered_payments_of_same_method) == 1