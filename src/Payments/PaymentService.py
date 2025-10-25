import json
from Payments.Payment import Payment
from Payments.PaymentMethod import PaymentMethod, try_get_payment_method
from Payments.PaymentValidationStrategies.PaymentMethodValidationStrategyFactory import PaymentMethodValidationStrategyFactory
from Payments.PaymentStatus import PaymentStatus

_validation_factory = PaymentMethodValidationStrategyFactory()

class PaymentService:
    def __init__(self, data_path: str):
        """Init service and load persisted payments."""
        self.data_path = data_path
        self.payments: dict[str, Payment] = self._load_from_disk()

    def load_all_payments(self) -> dict[str, Payment]:
        """Return a shallow copy of payments."""
        return dict(self.payments)

    def create_payment(self, payment_id: str, amount: float, payment_method) -> Payment:
        """Create and persist a new payment."""
        if payment_id in self.payments:
            raise ValueError("Payment with this ID already exists")
        if not isinstance(payment_method, PaymentMethod):
            ok, pm = try_get_payment_method(payment_method)
            if not ok:
                raise ValueError("invalid payment_method")
            payment_method = pm
        new = Payment(payment_id=payment_id, amount=amount, payment_method=payment_method, status=PaymentStatus.REGISTRADO)
        self._save_all_payments(payment_id, new, dict(self.payments))
        return new
    
    def update_payment(self, payment_id: str, amount: float, payment_method) -> Payment:
        """Update mutable fields of a registered payment."""
        payment = self._get_payment(payment_id)
        if payment.status == PaymentStatus.REGISTRADO:
            payment.amount = amount
            payment.payment_method = payment_method
            self._save_all_payments(payment_id, payment, dict(self.payments))
        return payment

    def pay_payment(self, payment_id: str) -> Payment:
        """Process payment and set status to PAGADO or FALLIDO."""
        payment = self._get_payment(payment_id)
        if payment.status != PaymentStatus.REGISTRADO:
            raise ValueError("Payment invalid status for payment")
        strategy = _validation_factory.get(payment.payment_method)
        if strategy is None:
             raise ValueError("Invalid payment method")
        ok = strategy.validate(payment, list(self.payments.values()))
        payment.status = PaymentStatus.PAGADO if ok else PaymentStatus.FALLIDO
        self._save_all_payments(payment_id, payment, dict(self.payments))
        return payment

    def revert_payment(self, payment_id: str) -> Payment:
        """Revert a failed payment to REGISTRADO."""
        payment = self._get_payment(payment_id)
        if payment.status == PaymentStatus.FALLIDO:
            payment.status = PaymentStatus.REGISTRADO
            self._save_all_payments(payment_id, payment, dict(self.payments))
        return payment

    def _load_from_disk(self) -> dict[str, Payment]:
        """Read payments from disk, skip invalid entries."""
        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            payments: dict[str, Payment] = {}
            for pid, p_data in (raw_data or {}).items():
                try:
                    payments[pid] = Payment(payment_id=pid, **p_data)
                except Exception:
                    continue
            return payments
        except FileNotFoundError:
            return {}

    def _get_payment(self, payment_id: str) -> Payment:
        """Return payment by id or raise KeyError."""
        if payment_id not in self.payments:
            raise KeyError("Payment not found")
        return self.payments[payment_id]
    
    def _save_all_payments(self, payment_id: str, payment: Payment, payments_dict: dict | None = None) -> None:
        """Persist payments to disk (overwrites file)."""
        if payments_dict is None:
            payments_dict = self.payments
        payments_dict[payment_id] = payment
        self.payments = payments_dict
        serializable_data = {}
        for pid, p in self.payments.items():
            if hasattr(p, "model_dump"):
                serializable_data[pid] = p.model_dump()
            elif hasattr(p, "dict"):
                serializable_data[pid] = p.dict()
            else:
                serializable_data[pid] = vars(p)
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(serializable_data, f, indent=4, ensure_ascii=False)