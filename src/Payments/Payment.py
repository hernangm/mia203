from pydantic import BaseModel
from Payments.PaymentMethod import PaymentMethod
from Payments.PaymentStatus import PaymentStatus

class Payment(BaseModel):
    """
    Represents a payment transaction.

    Attributes:
        payment_id (str): Unique identifier for the payment.
        amount (float): Amount to be paid.
        payment_method (PaymentMethod): Method used for payment.
        status (PaymentStatus): Current status of the payment.
    """
    payment_id: str
    amount: float
    payment_method: PaymentMethod
    status: PaymentStatus