from fastapi import FastAPI, HTTPException, Path, Query
from paymentService import PaymentService
from constants import (
	STATUS,
	AMOUNT,
	PAYMENT_METHOD,
	STATUS_REGISTRADO,
	STATUS_PAGADO,
	STATUS_FALLIDO,
	DATA_PATH,
)

app = FastAPI()
payment_service = PaymentService(DATA_PATH)


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
	payment_service.save_payment(pid, amount, payment_method, STATUS_REGISTRADO)
	return {"payment_id": pid, AMOUNT: amount, PAYMENT_METHOD: payment_method, STATUS: STATUS_REGISTRADO}


@app.post("/payments/{payment_id}/update")
async def update_payment(
	payment_id: str = Path(..., description="ID del pago"),
	amount: float = Query(..., description="Nuevo monto"),
	payment_method: str = Query(..., description="Nuevo método de pago"),
):
	"""Actualiza la información de un pago existente."""
	payments = payment_service.load_all_payments()
	pid = str(payment_id)
	if pid not in payments:
		raise HTTPException(status_code=404, detail="Payment not found")
	payments[pid][AMOUNT] = amount
	payments[pid][PAYMENT_METHOD] = payment_method
	payment_service.save_all_payments(payments)
	return payments[pid]


@app.post("/payments/{payment_id}/pay")
async def pay_payment(payment_id: str = Path(..., description="ID del pago")):
	"""Marca un pago como pagado."""
	payments = payment_service.load_all_payments()
	pid = str(payment_id)
	if pid not in payments:
		raise HTTPException(status_code=404, detail="Payment not found")
	if payments[pid].get(STATUS) == STATUS_PAGADO:
		raise HTTPException(status_code=400, detail="Payment already paid")
	payments[pid][STATUS] = STATUS_PAGADO
	payment_service.save_all_payments(payments)
	return payments[pid]


@app.post("/payments/{payment_id}/revert")
async def revert_payment(payment_id: str = Path(..., description="ID del pago")):
	"""Revierte un pago al estado registrado."""
	payments = payment_service.load_all_payments()
	pid = str(payment_id)
	if pid not in payments:
		raise HTTPException(status_code=404, detail="Payment not found")
	payments[pid][STATUS] = STATUS_REGISTRADO
	payment_service.save_all_payments(payments)
	return payments[pid]
