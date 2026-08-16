from decimal import Decimal

from django.conf import settings
from django.db import models

from catalog.models import Product
from catalog.pricing import effective_price


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
        null=True,
        blank=True,
        verbose_name="utilizador",
    )
    session_key = models.CharField(
        "chave da sessão",
        max_length=40,
        unique=True,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "carrinho"
        verbose_name_plural = "carrinhos"

    def __str__(self):
        identity = self.user or self.session_key or self.pk
        return f"Carrinho {identity}"

    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        return sum((item.line_total for item in self.items.select_related("product")), Decimal("0.00"))

    def grouped_by_store(self):
        groups = {}
        for item in self.items.select_related("product__store", "product__category"):
            groups.setdefault(item.product.store, []).append(item)
        return groups


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="carrinho",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items",
        verbose_name="produto",
    )
    quantity = models.PositiveIntegerField("quantidade", default=1)
    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"],
                name="unique_product_per_cart",
            )
        ]
        ordering = ["created_at"]
        verbose_name = "item do carrinho"
        verbose_name_plural = "itens do carrinho"

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def line_total(self):
        return effective_price(self.product) * self.quantity
