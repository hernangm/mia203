from pathlib import Path

from fastapi import FastAPI, HTTPException, Path as FPath, Query, status

from Payments.PaymentService import PaymentService

# Ensure a reproducible data path relative to this file
_data_dir = Path(__file__).resolve().parent / "data"
_data_dir.mkdir(exist_ok=True)
_data_file = str(_data_dir / "payments.json")

app = FastAPI()
payment_service = PaymentService(_data_file)


@app.get("/payments")
async def get_payments():
    """Retrieve all payments in the system."""
    try:
        return payment_service.load_all_payments()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/payments/{payment_id}", status_code=status.HTTP_201_CREATED)
async def register_payment(
    payment_id: str = FPath(..., description="Payment ID"),
    amount: float = Query(..., description="Payment amount"),
    payment_method: str = Query(..., description="Payment method"),
):
    """Register a payment with its information."""
    try:
        return payment_service.register_payment(payment_id, amount, payment_method)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/payments/{payment_id}/update")
async def update_payment(
    payment_id: str = FPath(..., description="Payment ID"),
    amount: float = Query(..., description="New amount"),
    payment_method: str = Query(..., description="New payment method"),
):
    """Update the information of an existing payment."""
    try:
        return payment_service.update_payment(payment_id, amount, payment_method)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/payments/{payment_id}/pay")
async def pay_payment(payment_id: str = FPath(..., description="Payment ID")):
    """Mark a payment as paid."""
    try:
        return payment_service.pay_payment(payment_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/payments/{payment_id}/revert")
async def revert_payment(payment_id: str = FPath(..., description="Payment ID")):
    """Revert a payment back to the registered state."""
    try:
        return payment_service.revert_payment(payment_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
