import json
from Payments.Payment import Payment
from Payments.PaymentMethod import PaymentMethod, try_get_payment_method
from Payments.PaymentValidationStrategies.PaymentMethodValidationStrategyFactory import PaymentMethodValidationStrategyFactory

# instantiate once
_validation_factory = PaymentMethodValidationStrategyFactory()

class PaymentService:
    def __init__(self, data_path: str):
        self.data_path = data_path
        # Carga los pagos en memoria una sola vez al inicializar
        self.payments: dict[str, Payment] = self._load_from_disk()

    def load_all_payments(self) -> dict[str, Payment]:
        """Devuelve el diccionario en memoria (copia superficial)."""
        return dict(self.payments)

    def register_payment(self, payment_id: str, amount: float, payment_method) -> Payment:
        """Registra un nuevo pago, validando que no exista previamente."""
        if payment_id in self.payments:
            raise ValueError("Payment with this ID already exists")
        if not isinstance(payment_method, PaymentMethod):
            ok, pm = try_get_payment_method(payment_method)
            if not ok:
                raise ValueError("invalid payment_method")
            payment_method = pm
        new = Payment(payment_id=payment_id, amount=amount, payment_method=payment_method, status=constants.STATUS_REGISTRADO)
        self._save_all_payments(payment_id, new, dict(self.payments))
        return new
    
    def update_payment(self, payment_id: str, amount: float, payment_method) -> Payment:
        """Actualiza un pago existente si su estado es 'REGISTRADO'."""
        payment = self._get_payment(payment_id)
        if payment.status == constants.STATUS_REGISTRADO:
            payment.amount = amount
            payment.payment_method = payment_method
            self._save_all_payments(payment_id, payment, dict(self.payments))
        return payment

    def pay_payment(self, payment_id: str) -> Payment:
        """Procesa el pago de un registro, cambiando su estado a PAGADO o FALLIDO."""
        payment = self._get_payment(payment_id)
        if payment.status != constants.STATUS_REGISTRADO:
            raise ValueError("Payment invalid status for payment")
        strategy = _validation_factory.get(payment.payment_method)
        if strategy is None:
            raise ValueError("Invalid payment method")
        ok = strategy.validate(payment, list(self.payments.values()))
        payment.status = constants.STATUS_PAGADO if ok else constants.STATUS_FALLIDO
        self._save_all_payments(payment_id, payment, dict(self.payments))
        return payment

    def revert_payment(self, payment_id: str) -> Payment:
        """Revierte un pago fallido al estado 'REGISTRADO'."""
        payment = self._get_payment(payment_id)
        if payment.status == constants.STATUS_FALLIDO:
            payment.status = constants.STATUS_REGISTRADO
            self._save_all_payments(payment_id, payment, dict(self.payments))
        return payment

    # Métodos privados colocados al final
    def _load_from_disk(self) -> dict[str, Payment]:
        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            # Itera sobre los pares (id, datos) del diccionario y crea objetos Payment
            return {pid: Payment(payment_id=pid, **p_data) for pid, p_data in raw_data.items()}
        except FileNotFoundError:
            return {}

    def _get_payment(self, payment_id: str) -> Payment:
        """Método privado para obtener un pago específico del diccionario en memoria."""
        if payment_id not in self.payments:
            raise KeyError("Payment not found")
        return self.payments[payment_id]
    
    def _save_all_payments(self, payment_id: str, payment: Payment, payments_dict: dict | None = None) -> None:
        """Actualiza la entrada en memoria y persiste todos los pagos en el archivo JSON."""
        # update memory and persist
        if payments_dict is None:
            payments_dict = self.payments
        payments_dict[payment_id] = payment
        self.payments = payments_dict
        # Convierte los objetos Payment de vuelta a diccionarios para la serialización JSON
        serializable_data = {pid: p.model_dump() for pid, p in self.payments.items()}
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(serializable_data, f, indent=4, ensure_ascii=False)