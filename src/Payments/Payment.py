from pydantic import BaseModel
from Payments.PaymentMethod import PaymentMethod
from Payments.PaymentStatus import PaymentStatus

class Payment(BaseModel):
    payment_id: str
    amount: float
    payment_method: PaymentMethod
    status: PaymentStatus