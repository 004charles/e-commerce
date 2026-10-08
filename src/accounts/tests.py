from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from catalog.models import Category, Product
from orders.models import Order, OrderItem, StoreOrder
from stores.models import Store

from .models import User


class AccountOrderTests(TestCase):
    def setUp(self):
        self.customer = User.objects.create_user(
            username="customer-orders",
            email="customer@example.com",
            password="safe-password-123",
        )
        self.other_customer = User.objects.create_user(
            username="other-customer-orders",
            email="other@example.com",
            password="safe-password-123",
        )
        owner = User.objects.create_user(
            username="account-store-owner",
            email="store@example.com",
            password="safe-password-123",
            role=User.Role.STORE_OWNER,
        )
        store = Store.objects.create(
            owner=owner,
            name="Loja da Conta",
            slug="loja-da-conta",
            province="Luanda",
            municipality="Viana",
            status=Store.Status.APPROVED,
        )
        category = Category.objects.create(name="Conta", slug="conta")
        product = Product.objects.create(
            store=store,
            category=category,
            name="Produto da Conta",
            slug="produto-da-conta",
            sku="ACCOUNT-001",
            price=Decimal("12000.00"),
            stock=4,
            status=Product.Status.ACTIVE,
        )
        self.order = Order.objects.create(
            user=self.customer,
            order_number="MA-ACCOUNT001",
            customer_name="Cliente Conta",
            customer_email=self.customer.email,
            customer_phone="+244 923 000 000",
            province="Luanda",
            municipality="Viana",
            address="Rua da Conta",
            subtotal=Decimal("12000.00"),
            total=Decimal("12000.00"),
            status=Order.Status.AWAITING_PAYMENT,
        )
        store_order = StoreOrder.objects.create(
            order=self.order,
            store=store,
            subtotal=Decimal("12000.00"),
            total=Decimal("12000.00"),
            status=Order.Status.AWAITING_PAYMENT,
        )
        OrderItem.objects.create(
            store_order=store_order,
            product=product,
            product_name=product.name,
            sku=product.sku,
            store_name=store.name,
            unit_price=product.price,
            quantity=1,
            line_total=product.price,
        )
        self.other_order = Order.objects.create(
            user=self.other_customer,
            order_number="MA-OTHER001",
            customer_name="Outro Cliente",
            customer_email=self.other_customer.email,
            customer_phone="+244 923 000 001",
            province="Luanda",
            municipality="Cazenga",
            address="Rua do Outro Cliente",
            subtotal=Decimal("1.00"),
            total=Decimal("1.00"),
        )

    def test_customer_sees_only_own_orders(self):
        self.client.force_login(self.customer)

        response = self.client.get(reverse("accounts:order-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order.order_number)
        self.assertNotContains(response, self.other_order.order_number)

    def test_customer_can_open_own_order_detail(self):
        self.client.force_login(self.customer)

        response = self.client.get(
            reverse("accounts:order-detail", kwargs={"order_number": self.order.order_number})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Produto da Conta")

    def test_customer_cannot_open_other_customer_order(self):
        self.client.force_login(self.customer)

        response = self.client.get(
            reverse("accounts:order-detail", kwargs={"order_number": self.other_order.order_number})
        )

        self.assertEqual(response.status_code, 404)

    def test_logout_ends_session(self):
        self.client.force_login(self.customer)

        response = self.client.post(reverse("accounts:logout"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["ok"])
        session_response = self.client.get(reverse("accounts:profile"))
        self.assertEqual(session_response.status_code, 401)


class AdminDashboardTests(TestCase):
    def test_staff_can_view_admin_metrics(self):
        admin = User.objects.create_superuser(
            username="admin-metrics",
            email="admin-metrics@example.ao",
            password="safe-password-123",
        )
        self.client.force_login(admin)

        response = self.client.get("/admin/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Visão geral do Marketplace Angola")
        self.assertContains(response, "Lojas aprovadas")
        self.assertContains(response, "Pagamentos pendentes")

    def test_customer_cannot_view_admin_dashboard(self):
        customer = User.objects.create_user(
            username="admin-customer",
            email="admin-customer@example.ao",
            password="safe-password-123",
        )
        self.client.force_login(customer)

        response = self.client.get("/admin/")

        self.assertEqual(response.status_code, 302)
