from pathlib import Path

from fastapi import FastAPI, HTTPException, Path as FPath, Query, status

from Payments.PaymentService import PaymentService
from typing import List, Any
from Payments.Payment import Payment

# Ensure a reproducible data path relative to this file
_data_dir = Path(__file__).resolve().parent / "data"
_data_dir.mkdir(exist_ok=True)
_data_file = str(_data_dir / "payments.json")

app = FastAPI()
payment_service = PaymentService(_data_file)


@app.get("/payments")
async def get_all_payments() -> List[Payment]:
    """
    Returns a list of all payments.
    Response: List[Payment]
    """
    try:
        return payment_service.load_all_payments()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/payments/{payment_id}", status_code=status.HTTP_201_CREATED)
async def create_payment(
    payment_id: str = FPath(..., description="Payment ID"),
    amount: float = Query(..., description="Payment amount"),
    payment_method: str = Query(..., description="Payment method"),
) -> Payment:
    """
    Registers a new payment.
    Request: {amount: float, payment_method: str}
    Response: Payment
    """
    try:
        return payment_service.create_payment(payment_id, amount, payment_method)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/payments/{payment_id}/update")
async def update_payment(
    payment_id: str = FPath(..., description="Payment ID"),
    amount: float | None = None,
    payment_method: str | None = None,
) -> Payment:
    """
    Updates payment parameters.
    Request: {amount: float?, payment_method: str?}
    Response: Payment
    """
    try:
        return payment_service.update_payment(payment_id, amount, payment_method)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/payments/{payment_id}/pay")
async def pay_payment(payment_id: str = FPath(..., description="Payment ID")) -> Payment:
    """
    Attempts to process the payment.
    Response: PaymentStatus
    """
    try:
        return payment_service.pay_payment(payment_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/payments/{payment_id}/revert")
async def revert_payment(payment_id: str = FPath(..., description="Payment ID")) -> Payment:
    """
    Reverts the payment if possible.
    Response: PaymentStatus
    """
    try:
        return payment_service.revert_payment(payment_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
