import unittest
from unittest.mock import patch, mock_open, MagicMock
import json

from PaymentService import PaymentService
from Payment import Payment


class TestPaymentService(unittest.TestCase):

    def setUp(self):
        self.data_path = "test_data.json"
        self.service = PaymentService(self.data_path)
        self.sample_payment = Payment(amount=100.0, payment_method="Tarjeta", status="REGISTRADO")

    # -------------------------------------------------------
    # Test: load_all_payments (archivo existente)
    # -------------------------------------------------------
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        "1": {"amount": 100.0, "payment_method": "Tarjeta", "status": "REGISTRADO"}
    }))
    def test_load_all_payments_ok(self, mock_file):
        data = self.service.load_all_payments()
        self.assertIn("1", data)
        self.assertIsInstance(data["1"], Payment)
        self.assertEqual(data["1"].amount, 100.0)
        mock_file.assert_called_once_with(self.data_path, "r", encoding="utf-8")

    # -------------------------------------------------------
    # Test: load_all_payments (archivo no existe)
    # -------------------------------------------------------
    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_all_payments_file_not_found(self, mock_file):
        data = self.service.load_all_payments()
        self.assertEqual(data, {})  # Debe retornar diccionario vacío

    # -------------------------------------------------------
    # Test: save_all_payments
    # -------------------------------------------------------
    @patch("builtins.open", new_callable=mock_open)
    def test_save_all_payments(self, mock_file):
        payments = {"1": self.sample_payment}
        self.service.save_all_payments(payments)
        mock_file.assert_called_once_with(self.data_path, "w", encoding="utf-8")

        # Verifica que se haya escrito JSON válido
        handle = mock_file()
        written_data = json.loads(handle.write.call_args[0][0])
        self.assertIn("1", written_data)
        self.assertEqual(written_data["1"]["status"], "REGISTRADO")

    # -------------------------------------------------------
    # Test: load_payment
    # -------------------------------------------------------
    @patch.object(PaymentService, "load_all_payments", return_value={"1": Payment(amount=100, payment_method="Tarjeta", status="REGISTRADO")})
    def test_load_payment(self, mock_load_all):
        payment = self.service.load_payment("1")
        self.assertIsInstance(payment, Payment)
        self.assertEqual(payment.amount, 100)
        mock_load_all.assert_called_once()

    # -------------------------------------------------------
    # Test: save_payment_data
    # -------------------------------------------------------
    @patch.object(PaymentService, "load_all_payments", return_value={})
    @patch.object(PaymentService, "save_all_payments")
    def test_save_payment_data(self, mock_save_all, mock_load_all):
        payment = self.sample_payment
        self.service.save_payment_data("1", payment)
        mock_load_all.assert_called_once()
        mock_save_all.assert_called_once()
        args, _ = mock_save_all.call_args
        self.assertIn("1", args[0])
        self.assertIsInstance(args[0]["1"], Payment)

    # -------------------------------------------------------
    # Test: save_payment
    # -------------------------------------------------------
    @patch.object(PaymentService, "save_payment_data")
    def test_save_payment(self, mock_save_payment_data):
        self.service.save_payment("1", 500.0, "PayPal", "PAGADO")
        mock_save_payment_data.assert_called_once()
        args, _ = mock_save_payment_data.call_args
        self.assertEqual(args[0], "1")  # payment_id
        self.assertIsInstance(args[1], Payment)
        self.assertEqual(args[1].status, "PAGADO")


if __name__ == "__main__":
    unittest.main()
