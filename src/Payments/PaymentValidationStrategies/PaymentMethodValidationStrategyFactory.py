from typing import Optional
from .PayPalValidationStrategy import PayPalValidationStrategy
from .CreditCardValidationStrategy import CreditCardValidationStrategy
from ..PaymentMethod import PaymentMethod
from .BasePaymentMethodValidationStrategy import BasePaymentMethodValidationStrategy

class PaymentMethodValidationStrategyFactory:
    def __init__(self) -> None:
        self._registry: dict[PaymentMethod, BasePaymentMethodValidationStrategy] = {
            PaymentMethod.PAYPAL: PayPalValidationStrategy(),
            PaymentMethod.CREDIT_CARD: CreditCardValidationStrategy(),
        }

    def get(self, payment_method: PaymentMethod) -> Optional[BasePaymentMethodValidationStrategy]:
        """Return the corresponding strategy or None if it does not exist."""
        return self._registry.get(payment_method)

