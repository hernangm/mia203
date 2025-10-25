import json
from Payment import Payment # Importa la clase Payment directamente

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

    def save_payment_data(self, payment_id: str, payment: Payment) -> None:
        all_data = self.load_all_payments()
        all_data[str(payment_id)] = payment
        self.save_all_payments(all_data)

    def save_payment(self, payment_id: str, amount: float, payment_method: str, status: str) -> None:
        # Crea un objeto Payment y lo guarda
        new_payment = Payment(amount=amount, payment_method=payment_method, status=status)
        self.save_payment_data(payment_id, new_payment)