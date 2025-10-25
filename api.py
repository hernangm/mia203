from fastapi import FastAPI, HTTPException, Path, Query
from paymentService import paymentService as ps
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


@app.get("/payments")   
async def get_payments():
	"""Obtiene todos los pagos del sistema."""
	return ps.load_all_payments()


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
	payments = ps.load_all_payments()
	pid = str(payment_id)
	if pid in payments:
		raise HTTPException(status_code=400, detail="Payment already exists")
	ps.save_payment(pid, amount, payment_method, STATUS_REGISTRADO)
	return {"payment_id": pid, AMOUNT: amount, PAYMENT_METHOD: payment_method, STATUS: STATUS_REGISTRADO}


@app.post("/payments/{payment_id}/update")
async def update_payment(
	payment_id: str = Path(..., description="ID del pago"),
	amount: float = Query(..., description="Nuevo monto"),
	payment_method: str = Query(..., description="Nuevo método de pago"),
):
	"""Actualiza la información de un pago existente."""
	payments = ps.load_all_payments()
	pid = str(payment_id)
	if pid not in payments:
		raise HTTPException(status_code=404, detail="Payment not found")
	payments[pid][AMOUNT] = amount
	payments[pid][PAYMENT_METHOD] = payment_method
	ps.save_all_payments(payments)
	return payments[pid]


@app.post("/payments/{payment_id}/pay")
async def pay_payment(payment_id: str = Path(..., description="ID del pago")):
	"""Marca un pago como pagado."""
	payments = ps.load_all_payments()
	pid = str(payment_id)
	if pid not in payments:
		raise HTTPException(status_code=404, detail="Payment not found")
	if payments[pid].get(STATUS) == STATUS_PAGADO:
		raise HTTPException(status_code=400, detail="Payment already paid")
	payments[pid][STATUS] = STATUS_PAGADO
	ps.save_all_payments(payments)
	return payments[pid]


@app.post("/payments/{payment_id}/revert")
async def revert_payment(payment_id: str = Path(..., description="ID del pago")):
	"""Revierte un pago al estado registrado."""
	payments = ps.load_all_payments()
	pid = str(payment_id)
	if pid not in payments:
		raise HTTPException(status_code=404, detail="Payment not found")
	payments[pid][STATUS] = STATUS_REGISTRADO
	ps.save_all_payments(payments)
	return payments[pid]
