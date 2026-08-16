from django.urls import reverse
from django.test import TestCase

from accounts.models import User
from catalog.models import Category, Product
from stores.models import Store


class MarketplaceSearchTests(TestCase):
    def setUp(self):
        owner = User.objects.create_user(
            username="search-owner",
            email="search-owner@example.com",
            password="safe-password-123",
            role=User.Role.STORE_OWNER,
        )
        self.store = Store.objects.create(
            owner=owner,
            name="Loja Pesquisa Luanda",
            slug="loja-pesquisa-luanda",
            province="Luanda",
            municipality="Viana",
            status=Store.Status.APPROVED,
        )
        category = Category.objects.create(name="Telemóveis", slug="telemoveis")
        Product.objects.create(
            store=self.store,
            category=category,
            name="Smartphone Pesquisa Pro",
            slug="smartphone-pesquisa-pro",
            sku="SEARCH-001",
            price="45000.00",
            stock=10,
            status=Product.Status.ACTIVE,
        )
        Product.objects.create(
            store=self.store,
            category=category,
            name="Produto sem stock",
            slug="produto-sem-stock",
            sku="SEARCH-002",
            price="1000.00",
            stock=0,
            status=Product.Status.ACTIVE,
        )

    def test_search_returns_product_store_location_and_price(self):
        response = self.client.get(reverse("homepage:search-data"), {"q": "smartphone pesquisa"})

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["count"], 1)
        result = payload["results"][0]
        self.assertEqual(result["name"], "Smartphone Pesquisa Pro")
        self.assertEqual(result["store"], "Loja Pesquisa Luanda")
        self.assertEqual(result["location"], "Viana, Luanda")
        self.assertEqual(result["price"], "45000.00")

    def test_search_by_store_name_excludes_out_of_stock_products(self):
        response = self.client.get(reverse("homepage:search-data"), {"q": "Loja Pesquisa"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
