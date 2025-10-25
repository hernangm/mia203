import json
from Payment import Payment # Importa la clase Payment directamente
import constants
import paymentStrategies.paymentStrategyFactory as paymentStrategyFactory 

class PaymentService:
    def __init__(self, data_path: str):
        self.data_path = data_path

    def load_all_payments(self) -> dict[str, Payment]:
        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            # Itera sobre los pares (id, datos) del diccionario y crea objetos Payment
            return {pid: Payment(payment_id=pid, **p_data) for pid, p_data in raw_data.items()}
        except FileNotFoundError:
            return {}

    def register_payment(self, payment_id: str, amount: float, payment_method: str) -> Payment:
        """Registra un nuevo pago, validando que no exista previamente."""
        payments = self.load_all_payments() # Corrected method call
        if payment_id in payments:
            raise ValueError("Payment with this ID already exists")

        # Crea un objeto Payment y lo guarda
        new_payment = Payment(amount=amount, payment_method=payment_method, status=constants.STATUS_REGISTRADO)
        self._save_all_payments(payment_id, new_payment, payments) # Corrected method call and passed the payments dict
        return new_payment
    
    def update_payment(self, payment_id: str, amount: float, payment_method: str) -> Payment:
        """Actualiza un pago existente si su estado es 'REGISTRADO'."""
        payments = self.load_all_payments() # Corrected method call
        payment = self._get_payment(payment_id, payments)
        if payment.status == constants.STATUS_REGISTRADO:
            payment.amount = amount
            payment.payment_method = payment_method
            self._save_all_payments(payment_id, payment, payments)
        return payment

    def pay_payment(self, payment_id: str) -> Payment:
        """Procesa el pago de un registro, cambiando su estado a PAGADO o FALLIDO."""
        payments = self.load_all_payments() # Corrected method call
        payment = self._get_payment(payment_id, payments)
        if payment.status != constants.STATUS_REGISTRADO:
            raise ValueError("Payment invalid status for payment")
        validationStrategy = paymentStrategyFactory.get(payment.payment_method)
        if not validationStrategy:
            raise ValueError("Invalid payment method")
        if validationStrategy(payment, list(payments.values())):
            payment.status = constants.STATUS_PAGADO
        else:
            payment.status = constants.STATUS_FALLIDO
        self._save_all_payments(payment_id, payment, payments)
        return payment

    def revert_payment(self, payment_id: str) -> Payment:
        """Revierte un pago fallido al estado 'REGISTRADO'."""
        payments = self.load_all_payments() # Corrected method call
        payment = self._get_payment(payment_id, payments)
        if payment.status == constants.STATUS_FALLIDO:
            payment.status = constants.STATUS_REGISTRADO
            self._save_all_payments(payment_id, payment, payments)
        return payment
    
    def _get_payment(self, payment_id: str, payments: dict[str, Payment]) -> Payment:
        """Método privado para obtener un pago específico del diccionario de pagos."""
        if payment_id not in payments:
            raise KeyError("Payment not found")
        return payments[payment_id]
    
    def _save_all_payments(self, payment_id, payment, data: dict[str, Payment]) -> None:
        """Método privado para guardar todos los pagos en el archivo JSON."""
        data[payment_id] = payment
        # Convierte los objetos Payment de vuelta a diccionarios para la serialización JSON
        serializable_data = {pid: p.model_dump() for pid, p in data.items()}
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(serializable_data, f, indent=4, ensure_ascii=False)