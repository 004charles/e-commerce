from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from orders.models import Order

from .models import PaymentAttempt


class PaymentFlowTests(TestCase):
    def setUp(self):
        self.customer = User.objects.create_user(
            username="payment-customer",
            email="payment-customer@example.ao",
            password="safe-password-123",
        )
        self.other_customer = User.objects.create_user(
            username="payment-other",
            email="payment-other@example.ao",
            password="safe-password-123",
        )
        self.order = Order.objects.create(
            user=self.customer,
            order_number="MA-PAYMENT001",
            customer_name="Cliente Pagamento",
            customer_email=self.customer.email,
            customer_phone="923000000",
            province="Luanda",
            municipality="Viana",
            address="Rua de pagamento",
            subtotal=Decimal("1000.00"),
            total=Decimal("1000.00"),
            status=Order.Status.AWAITING_PAYMENT,
            payment_status=Order.PaymentStatus.NOT_STARTED,
        )

    def test_customer_can_select_method_and_attempt_remains_pending(self):
        self.client.force_login(self.customer)
        response = self.client.post(
            reverse("payments:select", kwargs={"order_number": self.order.order_number}),
            {"method": PaymentAttempt.Method.MULTICAIXA_EXPRESS},
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()["ok"])
        attempt = PaymentAttempt.objects.get(order=self.order)
        self.assertEqual(attempt.method, PaymentAttempt.Method.MULTICAIXA_EXPRESS)
        self.assertEqual(attempt.status, PaymentAttempt.Status.PENDING)
        self.assertEqual(self.order.payment_status, Order.PaymentStatus.NOT_STARTED)
        self.assertNotEqual(attempt.status, PaymentAttempt.Status.SUCCEEDED)

    def test_other_customer_cannot_select_payment_for_order(self):
        self.client.force_login(self.other_customer)
        response = self.client.get(
            reverse("payments:select", kwargs={"order_number": self.order.order_number})
        )

        self.assertEqual(response.status_code, 404)
        self.assertFalse(response.json()["ok"])
        self.assertEqual(PaymentAttempt.objects.count(), 0)

    def test_payment_selection_displays_all_supported_methods(self):
        self.client.force_login(self.customer)
        response = self.client.get(
            reverse("payments:select", kwargs={"order_number": self.order.order_number})
        )

        labels = [method["label"] for method in response.json()["methods"]]
        self.assertIn("Multicaixa Express", labels)
        self.assertIn("Unitel Money", labels)
        self.assertIn("PayPay", labels)
