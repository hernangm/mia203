import json


class PaymentService:
    def __init__(self, data_path: str):
        self.data_path = data_path

    def load_all_payments(self) -> dict:
        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_all_payments(self, data: dict) -> None:
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def load_payment(self, payment_id: str) -> dict:
        all_data = self.load_all_payments()
        return all_data[str(payment_id)]

    def save_payment_data(self, payment_id: str, data: dict) -> None:
        all_data = self.load_all_payments()
        all_data[str(payment_id)] = data
        self.save_all_payments(all_data)

    def save_payment(self, payment_id: str, amount, payment_method, status) -> None:
        data = {
            "amount": amount,
            "payment_method": payment_method,
            "status": status,
        }
        self.save_payment_data(payment_id, data)