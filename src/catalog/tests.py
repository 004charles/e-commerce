from django.urls import reverse
from django.test import TestCase

from accounts.models import User
from stores.models import Store
from orders.models import Order, OrderItem, StoreOrder

from .models import Category, Product, Review


class VendorProductManagementTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="vendor-one",
            email="vendor-one@example.com",
            password="safe-password-123",
            role=User.Role.STORE_OWNER,
        )
        self.other_owner = User.objects.create_user(
            username="vendor-two",
            email="vendor-two@example.com",
            password="safe-password-123",
            role=User.Role.STORE_OWNER,
        )
        self.store = Store.objects.create(
            owner=self.owner,
            name="Loja Um",
            slug="loja-um",
            status=Store.Status.APPROVED,
        )
        self.other_store = Store.objects.create(
            owner=self.other_owner,
            name="Loja Dois",
            slug="loja-dois",
            status=Store.Status.APPROVED,
        )
        self.category = Category.objects.create(name="Eletrónica", slug="electronica")

    def product_data(self, **overrides):
        data = {
            "category": self.category.pk,
            "name": "Auriculares Bluetooth",
            "slug": "",
            "sku": "SKU-001",
            "short_description": "Som sem fios",
            "description": "Auriculares para uso diário.",
            "price": "12500.00",
            "compare_at_price": "15000.00",
            "stock": "10",
            "status": Product.Status.DRAFT,
        }
        data.update(overrides)
        return data

    def test_vendor_can_create_product_and_slug_is_generated(self):
        self.client.force_login(self.owner)
        response = self.client.post(reverse("stores:product-create"), self.product_data())

        self.assertRedirects(response, reverse("stores:dashboard"))
        product = Product.objects.get(store=self.store, sku="SKU-001")
        self.assertEqual(product.slug, "auriculares-bluetooth")
        self.assertEqual(product.stock, 10)

    def test_vendor_cannot_manage_another_store_product(self):
        product = Product.objects.create(
            store=self.other_store,
            category=self.category,
            name="Produto de outra loja",
            slug="produto-outra-loja",
            sku="SKU-OTHER",
            price="5000.00",
            stock=4,
        )
        self.client.force_login(self.owner)

        self.assertEqual(
            self.client.get(reverse("stores:product-edit", kwargs={"pk": product.pk})).status_code,
            404,
        )
        self.assertEqual(
            self.client.get(reverse("stores:product-delete", kwargs={"pk": product.pk})).status_code,
            404,
        )

    def test_vendor_can_update_owned_product_stock(self):
        product = Product.objects.create(
            store=self.store,
            category=self.category,
            name="Produto de stock",
            slug="produto-de-stock",
            sku="SKU-STOCK",
            price="5000.00",
            stock=4,
            status=Product.Status.ACTIVE,
        )
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse("stores:product-stock", kwargs={"pk": product.pk}),
            {"stock": "0"},
        )

        self.assertRedirects(response, reverse("stores:dashboard"))
        product.refresh_from_db()
        self.assertEqual(product.stock, 0)
        self.assertEqual(product.status, Product.Status.OUT_OF_STOCK)


class ProductReviewTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="review-vendor",
            email="review-vendor@example.com",
            password="safe-password-123",
            role=User.Role.STORE_OWNER,
        )
        self.customer = User.objects.create_user(
            username="review-customer",
            email="review-customer@example.com",
            password="safe-password-123",
            role=User.Role.CUSTOMER,
        )
        self.other_customer = User.objects.create_user(
            username="other-customer",
            email="other-customer@example.com",
            password="safe-password-123",
            role=User.Role.CUSTOMER,
        )
        self.store = Store.objects.create(
            owner=self.owner,
            name="Loja de Avaliações",
            slug="loja-avaliacoes",
            status=Store.Status.APPROVED,
        )
        self.category = Category.objects.create(name="Testes", slug="testes")
        self.product = Product.objects.create(
            store=self.store,
            category=self.category,
            name="Produto Avaliável",
            slug="produto-avaliavel",
            sku="REVIEW-001",
            price="1000.00",
            stock=10,
            status=Product.Status.ACTIVE,
        )
        order = Order.objects.create(
            user=self.customer,
            order_number="ORD-REVIEW-001",
            customer_name="Cliente Review",
            customer_email=self.customer.email,
            customer_phone="923000000",
            province="Luanda",
            municipality="Viana",
            address="Rua de teste",
            subtotal="1000.00",
            total="1000.00",
            status=Order.Status.COMPLETED,
            payment_status=Order.PaymentStatus.PAID,
        )
        store_order = StoreOrder.objects.create(
            order=order,
            store=self.store,
            subtotal="1000.00",
            total="1000.00",
            status=Order.Status.COMPLETED,
        )
        OrderItem.objects.create(
            store_order=store_order,
            product=self.product,
            product_name=self.product.name,
            sku=self.product.sku,
            store_name=self.store.name,
            unit_price=self.product.price,
            quantity=1,
            line_total=self.product.price,
        )

    def review_url(self):
        return reverse(
            "catalog:submit-review",
            kwargs={"store_slug": self.store.slug, "slug": self.product.slug},
        )

    def test_authenticated_customer_who_purchased_can_review(self):
        self.client.force_login(self.customer)
        response = self.client.post(
            self.review_url(), {"rating": "5", "comment": "Produto excelente."},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        self.product.refresh_from_db()
        self.assertEqual(self.product.review_count, 1)
        self.assertEqual(str(self.product.rating), "5.00")
        self.assertEqual(Review.objects.count(), 1)

    def test_customer_without_purchase_cannot_review(self):
        self.client.force_login(self.other_customer)
        response = self.client.post(
            self.review_url(), {"rating": "4", "comment": "Comentário não autorizado."},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Review.objects.count(), 0)

    def test_customer_cannot_submit_duplicate_review(self):
        Review.objects.create(product=self.product, user=self.customer, rating=4, comment="Muito bom.")
        self.client.force_login(self.customer)
        response = self.client.post(
            self.review_url(), {"rating": "5", "comment": "Segunda avaliação."},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(Review.objects.count(), 1)

    def test_product_detail_exposes_real_review_context(self):
        Review.objects.create(product=self.product, user=self.customer, rating=4, comment="Muito bom.")
        response = self.client.get(
            reverse("catalog:detail", kwargs={"store_slug": self.store.slug, "slug": self.product.slug})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"review_count": 1')


class ProductSEOTests(TestCase):
    def setUp(self):
        owner = User.objects.create_user(
            username="seo-owner",
            email="seo-owner@example.com",
            password="safe-password-123",
            role=User.Role.STORE_OWNER,
        )
        store = Store.objects.create(
            owner=owner,
            name="Loja SEO Angola",
            slug="loja-seo-angola",
            status=Store.Status.APPROVED,
        )
        category = Category.objects.create(name="Tecnologia", slug="tecnologia")
        self.product = Product.objects.create(
            store=store,
            category=category,
            name="Laptop Angola Pro",
            slug="laptop-angola-pro",
            sku="SEO-001",
            short_description="Laptop profissional para trabalho em Angola.",
            description="Descrição completa do laptop.",
            price="250000.00",
            stock=5,
            status=Product.Status.ACTIVE,
        )

    def test_product_detail_contains_dynamic_seo_metadata(self):
        response = self.client.get(
            reverse(
                "catalog:detail",
                kwargs={"store_slug": self.product.store.slug, "slug": self.product.slug},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<link rel=\"canonical\"", html=False)
        self.assertContains(response, self.product.get_absolute_url())
        self.assertContains(response, "og:type")
        self.assertContains(response, "https://schema.org")
        self.assertContains(response, "Laptop Angola Pro")
        self.assertContains(response, "AOA")
