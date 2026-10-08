from datetime import timedelta
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from cart.models import Cart, CartItem
from catalog.models import Category, Product, Promotion
from accounts.models import User
from stores.models import Store

from .models import Order, OrderItem, StoreOrder


class CheckoutTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Teste", slug="teste")
        self.stores = []
        for index, data in enumerate(
            [("Loja A", "Viana"), ("Loja B", "Cazenga")], start=1
        ):
            owner = User.objects.create_user(
                username=f"checkout-owner-{index}",
                email=f"owner-{index}@example.com",
                password="safe-password-123",
                role=User.Role.STORE_OWNER,
            )
            self.stores.append(
                Store.objects.create(
                    owner=owner,
                    name=data[0],
                    slug=f"loja-checkout-{index}",
                    province="Luanda",
                    municipality=data[1],
                    status=Store.Status.APPROVED,
                )
            )
        self.products = [
            Product.objects.create(
                store=self.stores[0],
                category=category,
                name="Produto A",
                slug="produto-a",
                sku="A-001",
                price=Decimal("10000.00"),
                stock=5,
                status=Product.Status.ACTIVE,
            ),
            Product.objects.create(
                store=self.stores[1],
                category=category,
                name="Produto B",
                slug="produto-b",
                sku="B-001",
                price=Decimal("7500.00"),
                stock=3,
                status=Product.Status.ACTIVE,
            ),
        ]
        self.client.get("/")
        self.cart = Cart.objects.create(session_key=self.client.session.session_key)
        CartItem.objects.create(cart=self.cart, product=self.products[0], quantity=2)
        CartItem.objects.create(cart=self.cart, product=self.products[1], quantity=1)

    def checkout_data(self):
        return {
            "customer_name": "Cliente Teste",
            "customer_email": "cliente@example.com",
            "customer_phone": "+244 923 000 000",
            "province": "Luanda",
            "municipality": "Viana",
            "address": "Rua de teste, 10",
            "address_details": "Perto do mercado",
            "notes": "Ligar antes da entrega",
        }

    def test_checkout_creates_parent_and_one_store_order_per_store(self):
        response = self.client.post(reverse("orders:checkout"), self.checkout_data())

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()["ok"])
        order = Order.objects.get()
        self.assertEqual(order.subtotal, Decimal("27500.00"))
        self.assertEqual(order.total, Decimal("27500.00"))
        self.assertEqual(order.status, Order.Status.AWAITING_PAYMENT)
        self.assertEqual(order.payment_status, Order.PaymentStatus.NOT_STARTED)
        self.assertEqual(StoreOrder.objects.filter(order=order).count(), 2)
        self.assertEqual(OrderItem.objects.filter(store_order__order=order).count(), 2)
        self.products[0].refresh_from_db()
        self.products[1].refresh_from_db()
        self.assertEqual(self.products[0].stock, 3)
        self.assertEqual(self.products[1].stock, 2)
        self.assertEqual(CartItem.objects.filter(cart=self.cart).count(), 0)

    def test_checkout_applies_active_product_promotion_server_side(self):
        now = timezone.now()
        Promotion.objects.create(
            name="Campanha de teste",
            discount_percent=Decimal("10.00"),
            starts_at=now - timedelta(days=1),
            ends_at=now + timedelta(days=1),
            product=self.products[0],
        )

        response = self.client.post(reverse("orders:checkout"), self.checkout_data())

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()["ok"])
        order = Order.objects.get()
        self.assertEqual(order.subtotal, Decimal("25500.00"))
        item = OrderItem.objects.get(product=self.products[0])
        self.assertEqual(item.unit_price, Decimal("9000.00"))
        self.assertEqual(item.line_total, Decimal("18000.00"))

    def test_expired_promotion_does_not_change_checkout_total(self):
        now = timezone.now()
        Promotion.objects.create(
            name="Campanha expirada",
            discount_percent=Decimal("50.00"),
            starts_at=now - timedelta(days=3),
            ends_at=now - timedelta(days=1),
            product=self.products[0],
        )

        response = self.client.post(reverse("orders:checkout"), self.checkout_data())

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()["ok"])
        order = Order.objects.get()
        self.assertEqual(order.subtotal, Decimal("27500.00"))

    def test_checkout_rejects_quantity_above_current_stock(self):
        CartItem.objects.filter(cart=self.cart, product=self.products[0]).update(quantity=99)

        response = self.client.post(reverse("orders:checkout"), self.checkout_data())

        self.assertEqual(response.status_code, 409)
        self.assertFalse(response.json()["ok"])
        self.assertEqual(Order.objects.count(), 0)
        self.products[0].refresh_from_db()
        self.assertEqual(self.products[0].stock, 5)
