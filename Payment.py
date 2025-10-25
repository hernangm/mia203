from pydantic import BaseModel

class Payment(BaseModel):
	amount: float
	payment_method: str
	status: str