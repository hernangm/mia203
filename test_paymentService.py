import unittest
from unittest.mock import patch, mock_open, MagicMock
import json

# Assuming these are in the same directory or accessible via PYTHONPATH
from paymentService import PaymentService
from Payment import Payment
import constants
# Mock the factory and strategies
from paymentStrategies import paymentStrategyFactory
from paymentStrategies import paypalStrategy
from paymentStrategies import creditcardStrategy

class TestPaymentService(unittest.TestCase):
    def setUp(self):
        self.test_data_path = "test_payments.json"
        self.service = PaymentService(self.test_data_path)
        self.initial_payments_data = {
            "001": {"amount": 100.0, "payment_method": "paypal", "status": constants.STATUS_REGISTRADO},
            "002": {"amount": 200.0, "payment_method": "credit_card", "status": constants.STATUS_PAGADO},
            "003": {"amount": 300.0, "payment_method": "paypal", "status": constants.STATUS_FALLIDO},
            "004": {"amount": 400.0, "payment_method": "credit_card", "status": constants.STATUS_REGISTRADO},
        }
        # Convert to Payment objects for internal service representation
        self.initial_payments_objects = {
            pid: Payment(**p_data) for pid, p_data in self.initial_payments_data.items()
        }

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_all_payments_success(self, mock_json_load, mock_file_open):
        mock_json_load.return_value = self.initial_payments_data
        payments = self.service.load_all_payments()
        mock_file_open.assert_called_once_with(self.test_data_path, "r", encoding="utf-8")
        self.assertEqual(len(payments), len(self.initial_payments_data))
        self.assertIsInstance(payments["001"], Payment)
        self.assertEqual(payments["001"].amount, 100.0)
        self.assertEqual(payments["001"].payment_method, "paypal")

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_all_payments_file_not_found(self, mock_file_open):
        payments = self.service.load_all_payments()
        mock_file_open.assert_called_once_with(self.test_data_path, "r", encoding="utf-8")
        self.assertEqual(payments, {})

    @patch.object(PaymentService, 'load_all_payments') # Patch the public method
    @patch.object(PaymentService, '_save_all_payments')
    def test_register_payment_success(self, mock_save_all_payments, mock_load_all_payments):
        mock_load_all_payments.return_value = self.initial_payments_objects.copy()
        new_payment_id = "005"
        new_amount = 500.0
        new_method = "bank_transfer"
        
        payment = self.service.register_payment(new_payment_id, new_amount, new_method)
        
        self.assertIsInstance(payment, Payment)
        self.assertEqual(payment.amount, new_amount)
        self.assertEqual(payment.payment_method, new_method)
        self.assertEqual(payment.status, constants.STATUS_REGISTRADO)
        
        # Verify _save_all_payments was called correctly
        # The 'payments' dict passed to _save_all_payments should include the new payment
        # The _save_all_payments method is responsible for adding it.
        original_payments_dict = self.initial_payments_objects.copy()
        mock_save_all_payments.assert_called_once_with(new_payment_id, payment, original_payments_dict)

    @patch.object(PaymentService, 'load_all_payments')
    def test_register_payment_duplicate_id(self, mock_load_all_payments):
        mock_load_all_payments.return_value = self.initial_payments_objects.copy()
        
        with self.assertRaisesRegex(ValueError, "Payment with this ID already exists"):
            self.service.register_payment("001", 100.0, "paypal")

    @patch.object(PaymentService, 'load_all_payments')
    @patch.object(PaymentService, '_save_all_payments')
    def test_update_payment_success(self, mock_save_all_payments, mock_load_all_payments):
        mock_loaded_payments = self.initial_payments_objects.copy()
        mock_load_all_payments.return_value = mock_loaded_payments
        
        payment_id_to_update = "001" # Status REGISTRADO
        new_amount = 150.0
        new_method = "new_method"
        
        updated_payment = self.service.update_payment(payment_id_to_update, new_amount, new_method)
        
        self.assertEqual(updated_payment.amount, new_amount)
        self.assertEqual(updated_payment.payment_method, new_method)
        self.assertEqual(updated_payment.status, constants.STATUS_REGISTRADO) # Status should not change
        
        # Verify _save_all_payments was called
        # The 'payments' dict passed to _save_all_payments should reflect the update
        expected_payments_dict_for_save = mock_loaded_payments.copy()
        expected_payments_dict_for_save[payment_id_to_update] = updated_payment # The object itself is modified
        mock_save_all_payments.assert_called_once_with(payment_id_to_update, updated_payment, expected_payments_dict_for_save)

    @patch.object(PaymentService, 'load_all_payments')
    @patch.object(PaymentService, '_save_all_payments')
    def test_update_payment_wrong_status(self, mock_save_all_payments, mock_load_all_payments):
        mock_loaded_payments = self.initial_payments_objects.copy()
        mock_load_all_payments.return_value = mock_loaded_payments
        
        payment_id_to_update = "002" # Status PAGADO
        new_amount = 250.0
        new_method = "new_method"
        
        original_payment = mock_loaded_payments[payment_id_to_update]
        updated_payment = self.service.update_payment(payment_id_to_update, new_amount, new_method)
        
        self.assertEqual(updated_payment.amount, original_payment.amount) # Should not change
        self.assertEqual(updated_payment.payment_method, original_payment.payment_method) # Should not change
        self.assertEqual(updated_payment.status, original_payment.status) # Should not change
        mock_save_all_payments.assert_not_called() # Should not save if not updated

    @patch.object(PaymentService, 'load_all_payments')
    def test_update_payment_not_found(self, mock_load_all_payments):
        mock_load_all_payments.return_value = self.initial_payments_objects.copy()
        
        with self.assertRaisesRegex(KeyError, "Payment not found"):
            self.service.update_payment("999", 100.0, "paypal")

    @patch('paymentStrategies.paymentStrategyFactory.get')
    @patch.object(PaymentService, 'load_all_payments')
    @patch.object(PaymentService, '_save_all_payments')
    def test_pay_payment_success(self, mock_save_all_payments, mock_load_all_payments, mock_get_strategy):
        mock_loaded_payments = self.initial_payments_objects.copy()
        mock_load_all_payments.return_value = mock_loaded_payments
        
        mock_get_strategy.return_value = MagicMock(return_value=True)
        
        payment_id_to_pay = "001" # Status REGISTRADO
        
        paid_payment = self.service.pay_payment(payment_id_to_pay)
        
        self.assertEqual(paid_payment.status, constants.STATUS_PAGADO)
        mock_get_strategy.return_value.assert_called_once_with(
            mock_loaded_payments[payment_id_to_pay], # The payment object itself
            list(mock_loaded_payments.values()) # All payment objects
        )
        
        expected_payments_dict_for_save = mock_loaded_payments.copy()
        expected_payments_dict_for_save[payment_id_to_pay] = paid_payment
        mock_save_all_payments.assert_called_once_with(payment_id_to_pay, paid_payment, expected_payments_dict_for_save)

    @patch('paymentStrategies.paymentStrategyFactory.get')
    @patch.object(PaymentService, 'load_all_payments')
    @patch.object(PaymentService, '_save_all_payments')
    def test_pay_payment_failed_validation(self, mock_save_all_payments, mock_load_all_payments, mock_get_strategy):
        mock_loaded_payments = self.initial_payments_objects.copy()
        mock_load_all_payments.return_value = mock_loaded_payments
        
        mock_get_strategy.return_value = MagicMock(return_value=False)
        
        payment_id_to_pay = "001" # Status REGISTRADO
        
        failed_payment = self.service.pay_payment(payment_id_to_pay)
        
        self.assertEqual(failed_payment.status, constants.STATUS_FALLIDO)
        mock_get_strategy.return_value.assert_called_once_with(
            mock_loaded_payments[payment_id_to_pay],
            list(mock_loaded_payments.values())
        )
        
        expected_payments_dict_for_save = mock_loaded_payments.copy()
        expected_payments_dict_for_save[payment_id_to_pay] = failed_payment
        mock_save_all_payments.assert_called_once_with(payment_id_to_pay, failed_payment, expected_payments_dict_for_save)

    @patch.object(PaymentService, 'load_all_payments')
    def test_pay_payment_invalid_status(self, mock_load_all_payments):
        mock_load_all_payments.return_value = self.initial_payments_objects.copy()
        
        with self.assertRaisesRegex(ValueError, "Payment invalid status for payment"):
            self.service.pay_payment("002") # Status PAGADO

    @patch('paymentStrategies.paymentStrategyFactory.get')
    @patch.object(PaymentService, 'load_all_payments')
    def test_pay_payment_invalid_method(self, mock_load_all_payments, mock_get_strategy):
        mock_load_all_payments.return_value = self.initial_payments_objects.copy()
        
        mock_get_strategy.return_value = None # Simulate unknown payment method
        
        payment_id_to_pay = "001"
        
        with self.assertRaisesRegex(ValueError, "Invalid payment method"):
            self.service.pay_payment(payment_id_to_pay)
        mock_get_strategy.assert_called_once_with(self.initial_payments_objects[payment_id_to_pay].payment_method)

    @patch.object(PaymentService, 'load_all_payments')
    def test_pay_payment_not_found(self, mock_load_all_payments):
        mock_load_all_payments.return_value = self.initial_payments_objects.copy()
        
        with self.assertRaisesRegex(KeyError, "Payment not found"):
            self.service.pay_payment("999")

    @patch.object(PaymentService, 'load_all_payments')
    @patch.object(PaymentService, '_save_all_payments')
    def test_revert_payment_success(self, mock_save_all_payments, mock_load_all_payments):
        mock_loaded_payments = self.initial_payments_objects.copy()
        mock_load_all_payments.return_value = mock_loaded_payments
        
        payment_id_to_revert = "003" # Status FALLIDO
        
        reverted_payment = self.service.revert_payment(payment_id_to_revert)
        
        self.assertEqual(reverted_payment.status, constants.STATUS_REGISTRADO)
        
        expected_payments_dict_for_save = mock_loaded_payments.copy()
        expected_payments_dict_for_save[payment_id_to_revert] = reverted_payment
        mock_save_all_payments.assert_called_once_with(payment_id_to_revert, reverted_payment, expected_payments_dict_for_save)

    @patch.object(PaymentService, 'load_all_payments')
    @patch.object(PaymentService, '_save_all_payments')
    def test_revert_payment_wrong_status(self, mock_save_all_payments, mock_load_all_payments):
        mock_loaded_payments = self.initial_payments_objects.copy()
        mock_load_all_payments.return_value = mock_loaded_payments
        
        payment_id_to_revert = "001" # Status REGISTRADO
        
        original_payment = mock_loaded_payments[payment_id_to_revert]
        reverted_payment = self.service.revert_payment(payment_id_to_revert)
        
        self.assertEqual(reverted_payment.status, original_payment.status) # Should not change
        mock_save_all_payments.assert_not_called() # Should not save if not reverted

    @patch.object(PaymentService, 'load_all_payments')
    def test_revert_payment_not_found(self, mock_load_all_payments):
        mock_load_all_payments.return_value = self.initial_payments_objects.copy()
        
        with self.assertRaisesRegex(KeyError, "Payment not found"):
            self.service.revert_payment("999")

    # Test _get_payment directly (though it's called by others)
    def test_get_payment_success(self):
        payments_dict = self.initial_payments_objects.copy()
        payment = self.service._get_payment("001", payments_dict)
        self.assertEqual(payment.amount, 100.0)
        self.assertEqual(payment.payment_method, "paypal")

    def test_get_payment_not_found(self):
        payments_dict = self.initial_payments_objects.copy()
        with self.assertRaisesRegex(KeyError, "Payment not found"):
            self.service._get_payment("999", payments_dict)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_all_payments(self, mock_json_dump, mock_file_open):
        payments_to_save = self.initial_payments_objects.copy()
        new_payment_id = "005"
        new_payment_obj = Payment(amount=500.0, payment_method="test", status=constants.STATUS_REGISTRADO)
        
        # Simulate adding a new payment to the data dict before saving
        data_to_pass_to_save = payments_to_save.copy()
        data_to_pass_to_save[new_payment_id] = new_payment_obj

        self.service._save_all_payments(new_payment_id, new_payment_obj, data_to_pass_to_save)
        
        mock_file_open.assert_called_once_with(self.test_data_path, "w", encoding="utf-8")
        
        # Check the data passed to json.dump
        expected_serializable_data = {
            pid: p.model_dump() for pid, p in data_to_pass_to_save.items()
        }
        mock_json_dump.assert_called_once_with(expected_serializable_data, mock_file_open(), indent=4, ensure_ascii=False)

if __name__ == '__main__':
    unittest.main()
