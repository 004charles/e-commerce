from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from catalog.models import Category, Product
from orders.models import Order, OrderItem, StoreOrder

from .models import Store, StoreApplication


class StoreApplicationFlowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="candidato",
            email="candidato@example.ao",
            password="SenhaSegura123!",
        )

    def test_application_requires_authentication(self):
        response = self.client.get(reverse("stores:apply"))
        self.assertEqual(response.status_code, 401)
        self.assertFalse(response.json()["ok"])

    def test_authenticated_user_can_submit_application(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("stores:apply"),
            {
                "proposed_name": "Loja de Teste",
                "description": "Uma loja para testes.",
                "phone": "+244900000000",
                "whatsapp": "+244900000000",
                "province": "Luanda",
                "municipality": "Talatona",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()["ok"])
        application = StoreApplication.objects.get()
        self.assertEqual(application.applicant, self.user)
        self.assertEqual(application.status, StoreApplication.Status.PENDING)


class StoreDashboardTests(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user(
            username="owner",
            email="owner@example.ao",
            password="SenhaSegura123!",
        )
        other_owner = get_user_model().objects.create_user(
            username="other-owner",
            email="other@example.ao",
            password="SenhaSegura123!",
        )
        self.category = Category.objects.create(name="Eletrónica", slug="eletronica")
        self.store = Store.objects.create(
            owner=self.owner,
            name="Loja do Proprietário",
            slug="loja-do-proprietario",
            status=Store.Status.APPROVED,
        )
        other_store = Store.objects.create(
            owner=other_owner,
            name="Outra Loja",
            slug="outra-loja",
            status=Store.Status.APPROVED,
        )
        Product.objects.create(
            store=self.store,
            category=self.category,
            name="Produto do proprietário",
            slug="produto-proprietario",
            sku="OWNER-1",
            price="100.00",
            stock=4,
            status=Product.Status.ACTIVE,
        )
        Product.objects.create(
            store=other_store,
            category=self.category,
            name="Produto de outra loja",
            slug="produto-outra-loja",
            sku="OTHER-1",
            price="200.00",
            stock=8,
            status=Product.Status.ACTIVE,
        )

    def test_dashboard_is_limited_to_current_owner(self):
        self.client.force_login(self.owner)
        response = self.client.get(reverse("stores:dashboard"))
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["store"]["name"], "Loja do Proprietário")
        names = [product["name"] for product in payload["products"]]
        self.assertIn("Produto do proprietário", names)
        self.assertNotIn("Produto de outra loja", names)


class VendorOrderManagementTests(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user(
            username="orders-owner",
            email="orders-owner@example.ao",
            password="SenhaSegura123!",
        )
        other_owner = get_user_model().objects.create_user(
            username="orders-other-owner",
            email="orders-other-owner@example.ao",
            password="SenhaSegura123!",
        )
        self.customer = get_user_model().objects.create_user(
            username="orders-customer",
            email="orders-customer@example.ao",
            password="SenhaSegura123!",
        )
        self.category = Category.objects.create(name="Pedidos", slug="pedidos")
        self.store = Store.objects.create(
            owner=self.owner,
            name="Loja dos Pedidos",
            slug="loja-dos-pedidos",
            status=Store.Status.APPROVED,
        )
        self.other_store = Store.objects.create(
            owner=other_owner,
            name="Outra Loja de Pedidos",
            slug="outra-loja-pedidos",
            status=Store.Status.APPROVED,
        )
        self.product = Product.objects.create(
            store=self.store,
            category=self.category,
            name="Produto Pedido",
            slug="produto-pedido",
            sku="ORDER-1",
            price="2500.00",
            stock=5,
            status=Product.Status.ACTIVE,
        )
        self.other_product = Product.objects.create(
            store=self.other_store,
            category=self.category,
            name="Produto de Outra Loja",
            slug="produto-outra-loja-pedidos",
            sku="ORDER-2",
            price="3500.00",
            stock=5,
            status=Product.Status.ACTIVE,
        )
        self.store_order = self._create_store_order(
            "ORD-VENDOR-001", self.store, self.product, Order.Status.AWAITING_PAYMENT
        )
        self.other_store_order = self._create_store_order(
            "ORD-VENDOR-002", self.other_store, self.other_product, Order.Status.AWAITING_PAYMENT
        )

    def _create_store_order(self, number, store, product, status):
        order = Order.objects.create(
            user=self.customer,
            order_number=number,
            customer_name="Maria dos Santos",
            customer_email="maria.santos@example.ao",
            customer_phone="923456789",
            province="Luanda",
            municipality="Viana",
            address="Rua do Mercado",
            subtotal=product.price,
            total=product.price,
            status=status,
        )
        store_order = StoreOrder.objects.create(
            order=order,
            store=store,
            subtotal=product.price,
            total=product.price,
            status=status,
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
        return store_order

    def test_dashboard_only_exposes_orders_from_owned_store(self):
        self.client.force_login(self.owner)
        response = self.client.get(reverse("stores:dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ORD-VENDOR-001")
        self.assertNotContains(response, "ORD-VENDOR-002")
        self.assertContains(response, "M*** d***")
        self.assertNotContains(response, "maria.santos@example.ao")

    def test_owner_can_update_owned_store_order_status(self):
        self.client.force_login(self.owner)
        response = self.client.post(
            reverse("stores:order-status", kwargs={"pk": self.store_order.pk}),
            {"status": Order.Status.PROCESSING},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], Order.Status.PROCESSING)
        self.store_order.refresh_from_db()
        self.assertEqual(self.store_order.status, Order.Status.PROCESSING)

    def test_owner_cannot_update_another_store_order(self):
        self.client.force_login(self.owner)
        response = self.client.post(
            reverse("stores:order-status", kwargs={"pk": self.other_store_order.pk}),
            {"status": Order.Status.PROCESSING},
        )

        self.assertEqual(response.status_code, 404)
        self.other_store_order.refresh_from_db()
        self.assertEqual(self.other_store_order.status, Order.Status.AWAITING_PAYMENT)

    def test_invalid_backward_transition_is_rejected(self):
        self.store_order.status = Order.Status.SHIPPED
        self.store_order.save(update_fields=["status"])
        self.client.force_login(self.owner)
        response = self.client.post(
            reverse("stores:order-status", kwargs={"pk": self.store_order.pk}),
            {"status": Order.Status.PROCESSING},
        )

        self.assertEqual(response.status_code, 409)
        self.assertFalse(response.json()["ok"])
        self.store_order.refresh_from_db()
        self.assertEqual(self.store_order.status, Order.Status.SHIPPED)
