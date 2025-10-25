from fastapi import FastAPI, HTTPException, Path, Query
from paymentService import PaymentService
import constants

app = FastAPI()
payment_service = PaymentService(constants.DATA_PATH)


@app.get("/payments")   
async def get_payments():
	"""Obtiene todos los pagos del sistema."""
	return payment_service.load_all_payments()


@app.post("/payments/{payment_id}")
async def register_payment(
	payment_id: str = Path(..., description="ID del pago"),
	amount: float = Query(..., description="Monto del pago"),
	payment_method: str = Query(..., description="Método de pago"),
):
	"""Registra un pago con su información.

	Args:
		payment_id: ID del pago (path)
		amount: monto (query)
		payment_method: método (query)
	"""
	payments = payment_service.load_all_payments()
	pid = str(payment_id)
	if pid in payments:
		raise HTTPException(status_code=400, detail="Payment already exists")
	payment = payment_service.save_payment(pid, amount, payment_method)
	return payment


@app.post("/payments/{payment_id}/update")
async def update_payment(
	payment_id: str = Path(..., description="ID del pago"),
	amount: float = Query(..., description="Nuevo monto"),
	payment_method: str = Query(..., description="Nuevo método de pago"),
):
	"""Actualiza la información de un pago existente."""
	payment = payment_service.update_payment(payment_id, amount, payment_method)
	return payment


@app.post("/payments/{payment_id}/pay")
async def pay_payment(payment_id: str = Path(..., description="ID del pago")):
	"""Marca un pago como pagado."""
	payment = payment_service.pay(payment_id)
	return payment


@app.post("/payments/{payment_id}/revert")
async def revert_payment(payment_id: str = Path(..., description="ID del pago")):
	"""Revierte un pago al estado registrado."""
	payment = payment_service.revert(payment_id)
	return payment
