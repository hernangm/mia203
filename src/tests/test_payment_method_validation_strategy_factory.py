import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Payments.PaymentValidationStrategies.PaymentMethodValidationStrategyFactory import PaymentMethodValidationStrategyFactory
from Payments.PaymentMethod import PaymentMethod
from Payments.PaymentValidationStrategies.PayPalValidationStrategy import PayPalValidationStrategy
from Payments.PaymentValidationStrategies.CreditCardValidationStrategy import CreditCardValidationStrategy

def test_get_returns_paypal_strategy():
    """
    Test that the factory returns a PayPalValidationStrategy instance for PaymentMethod.PAYPAL.
    """
    factory = PaymentMethodValidationStrategyFactory()
    strategy = factory.get(PaymentMethod.PAYPAL)
    assert isinstance(strategy, PayPalValidationStrategy)

def test_get_returns_credit_card_strategy():
    """
    Test that the factory returns a CreditCardValidationStrategy instance for PaymentMethod.CREDIT_CARD.
    """
    factory = PaymentMethodValidationStrategyFactory()
    strategy = factory.get(PaymentMethod.CREDIT_CARD)
    assert isinstance(strategy, CreditCardValidationStrategy)

def test_get_returns_none_for_unknown_method():
    """
    Test that the factory returns None when an unknown payment method is provided.
    """
    factory = PaymentMethodValidationStrategyFactory()
    class FakeMethod:
        pass
    strategy = factory.get(FakeMethod())
    assert strategy is None