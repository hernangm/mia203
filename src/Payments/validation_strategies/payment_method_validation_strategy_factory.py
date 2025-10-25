from typing import Optional, Dict
from payments import PaymentMethod
from payments.validation_strategies import BasePaymentMethodValidationStrategy, PayPalValidationStrategy, CreditCardValidationStrategy

class PaymentMethodValidationStrategyFactory:
    """
    Factory for retrieving payment method validation strategies.
    """
    def __init__(self) -> None:
        self._registry: Dict[PaymentMethod, BasePaymentMethodValidationStrategy] = {
            PaymentMethod.PAYPAL: PayPalValidationStrategy(),
            PaymentMethod.CREDIT_CARD: CreditCardValidationStrategy(),
        }

    def get(self, payment_method: PaymentMethod) -> Optional[BasePaymentMethodValidationStrategy]:
        """Return the corresponding strategy or None if it does not exist."""
        return self._registry.get(payment_method)

