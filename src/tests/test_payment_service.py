import sys
from pathlib import Path
# Make the repository "src" folder importable when running the test file directly.
# Path(__file__).resolve().parents[1] -> .../src
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import json
import pytest
from pathlib import Path

import Payments.PaymentService as ps_mod
from Payments.PaymentService import PaymentService
from Payments.PaymentStatus import PaymentStatus


class SimplePayment:
    def __init__(self, payment_id, amount, payment_method, status):
        self.payment_id = payment_id
        self.amount = amount
        self.payment_method = payment_method
        self.status = status

    # Serialization hook used by PaymentService._save_all_payments
    def model_dump(self):
        return {
            "payment_id": self.payment_id,
            "amount": self.amount,
            "payment_method": str(self.payment_method),
            "status": self.status.name if hasattr(self.status, "name") else str(self.status),
        }


class FakePM:
    def __repr__(self):
        return "<FakePM>"


def setup_simple_env(monkeypatch):
    # make PaymentService use simple classes so tests don't depend on other modules
    monkeypatch.setattr(ps_mod, "Payment", SimplePayment)
    # PaymentMethod type used for isinstance checks
    PMClass = FakePM
    monkeypatch.setattr(ps_mod, "PaymentMethod", PMClass)
    # try_get_payment_method returns a tuple (ok, instance)
    monkeypatch.setattr(ps_mod, "try_get_payment_method", lambda v: (True, PMClass()))


def read_payments_file(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def test_create_payment_succeeds(tmp_path, monkeypatch):
    setup_simple_env(monkeypatch)

    data_file = tmp_path / "payments.json"
    svc = PaymentService(str(data_file))

    created = svc.create_payment("p1", 10.5, "card")

    # returned object fields
    assert created.payment_id == "p1"
    assert created.amount == 10.5
    assert isinstance(created.payment_method, FakePM)
    assert created.status == PaymentStatus.REGISTRADO

    # persisted to disk
    persisted = read_payments_file(data_file)
    assert "p1" in persisted
    # amount as stored
    assert float(persisted["p1"]["amount"]) == pytest.approx(10.5)


def test_create_payment_duplicate_id_raises(tmp_path, monkeypatch):
    setup_simple_env(monkeypatch)

    data_file = tmp_path / "payments.json"
    svc = PaymentService(str(data_file))

    svc.create_payment("p1", 5.0, "card")

    with pytest.raises(ValueError):
        svc.create_payment("p1", 7.0, "card")