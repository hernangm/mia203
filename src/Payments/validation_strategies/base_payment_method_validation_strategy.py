from abc import ABC, abstractmethod
from typing import List
from payments import Payment

class BasePaymentMethodValidationStrategy(ABC):
    @abstractmethod
    def validate(self, payment: Payment, payments: List[Payment]) -> bool:
        """Validate a payment against strategy rules."""
        raise NotImplementedError