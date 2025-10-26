import json
import pytest
from pathlib import Path
from dataclasses import dataclass
from typing import Any
from payments import PaymentService, PaymentStatus, PaymentMethod
@dataclass
class SimplePayment:
    payment_id: str
    amount: float
    payment_method: Any
    status: Any

    def __repr__(self) -> str:
        return f"<SimplePayment id={self.payment_id} amount={self.amount!r}>"

    # Serialization hook used by PaymentService._save_all_payments
    def model_dump(self) -> dict:
        return {
            "payment_id": self.payment_id,
            "amount": float(self.amount),
            # If payment_method is an enum, prefer its name; fallback to string
            "payment_method": getattr(self.payment_method, "name", str(self.payment_method)),
            "status": getattr(self.status, "name", str(self.status)),
        }


def setup_simple_env(monkeypatch):
    """
    Monkeypatch payments module dependencies to use simple mock classes for isolated testing.
    """
    import payments
    # make PaymentService use simple classes so tests don't depend on other modules
    monkeypatch.setattr(payments, "Payment", SimplePayment, raising=False)
    # PaymentMethod type used for isinstance checks
    monkeypatch.setattr(payments, "PaymentMethod", PaymentMethod, raising=False)
    # try_get_payment_method returns a tuple (ok, instance)
    monkeypatch.setattr(payments, "try_get_payment_method", lambda v: (True, PaymentMethod.CREDIT_CARD), raising=False)


def read_payments_file(path: Path) -> dict:
    """
    Helper to read the payments file as a dictionary.
    """
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def test_create_payment_succeeds(tmp_path, monkeypatch):
    """
    Test that PaymentService.create_payment creates and persists a payment with correct fields.
    """
    setup_simple_env(monkeypatch)

    data_file = tmp_path / "payments.json"
    svc = PaymentService(str(data_file))

    created = svc.create_payment("p1", 10.5, PaymentMethod.CREDIT_CARD)

    # returned object fields
    assert created.payment_id == "p1"
    assert created.amount == 10.5
    assert isinstance(created.payment_method, PaymentMethod)
    assert created.status == PaymentStatus.REGISTRADO

    # persisted to disk
    persisted = read_payments_file(data_file)
    assert "p1" in persisted
    # amount as stored
    assert float(persisted["p1"]["amount"]) == pytest.approx(10.5)


def test_create_payment_duplicate_id_raises(tmp_path, monkeypatch):
    """
    Test that PaymentService.create_payment raises ValueError when payment_id already exists.
    """
    setup_simple_env(monkeypatch)

    data_file = tmp_path / "payments.json"
    svc = PaymentService(str(data_file))

    svc.create_payment("p1", 5.0, PaymentMethod.CREDIT_CARD)

    with pytest.raises(ValueError):
        svc.create_payment("p1", 7.0, PaymentMethod.CREDIT_CARD)