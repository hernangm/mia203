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
                # Convierte cada diccionario de pago en un objeto Payment
                return {pid: Payment(**p_data) for pid, p_data in raw_data.items()}
        except FileNotFoundError:
            return {}

    def save_all_payments(self, data: dict[str, Payment]) -> None:
        # Convierte los objetos Payment de vuelta a diccionarios para la serialización JSON
        serializable_data = {pid: p.model_dump() for pid, p in data.items()}
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(serializable_data, f, indent=4, ensure_ascii=False)

    def load_payment(self, payment_id: str) -> Payment:
        all_data = self.load_all_payments()
        return all_data[str(payment_id)]
    
    def update_payment(self, payment_id: str, amount: float, payment_method: str) -> Payment:
        payments = self.load_all_payments()
        pid = str(payment_id)
        if pid not in payments:
            raise Exception(status_code=404, detail="Payment not found")
        payment = payments[payment_id]
        if payment.status == constants.STATUS_REGISTRADO:
            payment.amount = amount
            payment.payment_method = payment_method
            payments[payment_id] = payment
            self.save_all_payments(payments)
        return payment

    def pay(self, payment_id: str) -> Payment:
        payments = self.load_all_payments()
        if payment_id not in payments:
            raise Exception(status_code=404, detail="Payment not found")
        payment = payments[payment_id]
        if payment.get(constants.STATUS) != constants.STATUS_REGISTRADO:
            raise Exception(status_code=400, detail="Payment invalid status for payment")
        validationStrategy = paymentStrategyFactory.get(payment.get(constants.PAYMENT_METHOD))
        if not validationStrategy:
            raise Exception(status_code=400, detail="Invalid payment method")
        if validationStrategy.validate(payment, payments):
            payment[constants.STATUS] = constants.STATUS_PAGADO
        else:
            payment[constants.STATUS] = constants.STATUS_FALLIDO
        payments[payment_id] = payment
        self.save_all_payments(payments)
        return payment

    def revert(self, payment_id: str) -> Payment:
        payments = self.load_all_payments()
        if payment_id not in payments:
            raise Exception(status_code=404, detail="Payment not found")
        payment = payments[payment_id]
        if payment.get(constants.STATUS) != constants.STATUS_FALLIDO:
            payment[constants.STATUS] = constants.STATUS_REGISTRADO
        payments[payment_id] = payment
        self.save_all_payments(payments)
        return payment
    
    def save_payment_data(self, payment_id: str, payment: Payment) -> None:
        all_data = self.load_all_payments()
        all_data[payment_id] = payment
        self.save_all_payments(all_data)

    def save_payment(self, payment_id: str, amount: float, payment_method: str) -> None:
        # Crea un objeto Payment y lo guarda
        new_payment = Payment(amount=amount, payment_method=payment_method, status=constants.STATUS_REGISTRADO)
        self.save_payment_data(payment_id, new_payment)
        return new_payment