from django.urls import reverse
from django.test import TestCase

from accounts.models import User
from catalog.models import Category, Product
from stores.models import Store

from .models import Cart, CartItem


class CartApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="cart-customer",
            email="cart-customer@example.com",
            password="safe-password-123",
        )
        owner = User.objects.create_user(
            username="cart-store-owner",
            email="cart-store@example.com",
            password="safe-password-123",
            role=User.Role.STORE_OWNER,
        )
        self.store = Store.objects.create(
            owner=owner,
            name="Loja do Carrinho",
            slug="loja-do-carrinho",
            status=Store.Status.APPROVED,
        )
        self.other_store = Store.objects.create(
            owner=owner,
            name="Outra Loja do Carrinho",
            slug="outra-loja-do-carrinho",
            status=Store.Status.APPROVED,
        )
        category = Category.objects.create(name="Demonstração", slug="demonstracao")
        self.product = Product.objects.create(
            store=self.store,
            category=category,
            name="Produto Carrinho Um",
            slug="produto-carrinho-um",
            sku="CART-001",
            price="1000.00",
            stock=5,
            status=Product.Status.ACTIVE,
        )
        self.other_product = Product.objects.create(
            store=self.other_store,
            category=category,
            name="Produto Carrinho Dois",
            slug="produto-carrinho-dois",
            sku="CART-002",
            price="2500.00",
            stock=3,
            status=Product.Status.ACTIVE,
        )

    def test_authenticated_customer_can_add_products_from_multiple_stores(self):
        self.client.force_login(self.user)
        first = self.client.post(reverse("cart:add"), {"product_id": self.product.pk, "quantity": 2})
        second = self.client.post(reverse("cart:add"), {"product_id": self.other_product.pk, "quantity": 1})

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 2)
        self.assertEqual(cart.total_quantity, 3)
        self.assertEqual(cart.subtotal, 4500)
        self.assertEqual(len(second.json()["cart"]["groups"]), 2)

    def test_stock_is_validated_on_server(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("cart:add"),
            {"product_id": self.product.pk, "quantity": 6},
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()["ok"])
        self.assertFalse(CartItem.objects.exists())

    def test_customer_can_update_and_remove_cart_item(self):
        self.client.force_login(self.user)
        self.client.post(reverse("cart:add"), {"product_id": self.product.pk, "quantity": 2})
        update = self.client.post(
            reverse("cart:update"),
            {"product_id": self.product.pk, "quantity": 4},
        )
        remove = self.client.post(
            reverse("cart:remove"),
            {"product_id": self.product.pk},
        )

        self.assertEqual(update.status_code, 200)
        self.assertEqual(update.json()["cart"]["item_count"], 4)
        self.assertEqual(remove.status_code, 200)
        self.assertEqual(remove.json()["cart"]["item_count"], 0)
