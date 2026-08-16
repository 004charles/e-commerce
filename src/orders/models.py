from decimal import Decimal

from django.conf import settings
from django.db import models

from stores.models import Store


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pendente"
        AWAITING_PAYMENT = "awaiting_payment", "A aguardar pagamento"
        PAID = "paid", "Pago"
        PROCESSING = "processing", "Em preparação"
        SHIPPED = "shipped", "Enviado"
        COMPLETED = "completed", "Concluído"
        CANCELLED = "cancelled", "Cancelado"

    class PaymentStatus(models.TextChoices):
        NOT_STARTED = "not_started", "Não iniciado"
        PENDING = "pending", "Pendente"
        PAID = "paid", "Pago"
        FAILED = "failed", "Falhou"
        REFUNDED = "refunded", "Reembolsado"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="orders",
        null=True,
        blank=True,
        verbose_name="utilizador",
    )
    session_key = models.CharField("chave da sessão", max_length=40, blank=True)
    order_number = models.CharField("número do pedido", max_length=24, unique=True)
    customer_name = models.CharField("nome do cliente", max_length=160)
    customer_email = models.EmailField("email do cliente")
    customer_phone = models.CharField("telefone do cliente", max_length=40)
    province = models.CharField("província", max_length=80)
    municipality = models.CharField("município", max_length=100)
    address = models.CharField("morada", max_length=240)
    address_details = models.CharField("detalhes da morada", max_length=240, blank=True)
    notes = models.TextField("observações", blank=True)
    subtotal = models.DecimalField("subtotal", max_digits=12, decimal_places=2, default=Decimal("0.00"))
    shipping_total = models.DecimalField("envio", max_digits=12, decimal_places=2, default=Decimal("0.00"))
    total = models.DecimalField("total", max_digits=12, decimal_places=2, default=Decimal("0.00"))
    currency = models.CharField("moeda", max_length=3, default="AOA")
    status = models.CharField(
        "estado",
        max_length=24,
        choices=Status.choices,
        default=Status.PENDING,
    )
    payment_status = models.CharField(
        "estado do pagamento",
        max_length=24,
        choices=PaymentStatus.choices,
        default=PaymentStatus.NOT_STARTED,
    )
    payment_method = models.CharField("método de pagamento", max_length=40, blank=True)
    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "pedido"
        verbose_name_plural = "pedidos"

    def __str__(self):
        return self.order_number


class StoreOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="store_orders")
    store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name="store_orders")
    subtotal = models.DecimalField("subtotal da loja", max_digits=12, decimal_places=2)
    shipping_total = models.DecimalField("envio da loja", max_digits=12, decimal_places=2, default=Decimal("0.00"))
    total = models.DecimalField("total da loja", max_digits=12, decimal_places=2)
    status = models.CharField(
        "estado",
        max_length=24,
        choices=Order.Status.choices,
        default=Order.Status.PENDING,
    )
    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["order", "store"], name="unique_store_order")
        ]
        verbose_name = "pedido da loja"
        verbose_name_plural = "pedidos das lojas"

    def __str__(self):
        return f"{self.order.order_number} — {self.store.name}"


class OrderItem(models.Model):
    store_order = models.ForeignKey(StoreOrder, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        "catalog.Product",
        on_delete=models.PROTECT,
        related_name="order_items",
        null=True,
        blank=True,
    )
    product_name = models.CharField("nome do produto", max_length=180)
    sku = models.CharField("SKU", max_length=80)
    store_name = models.CharField("nome da loja", max_length=160)
    unit_price = models.DecimalField("preço unitário", max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField("quantidade")
    line_total = models.DecimalField("total da linha", max_digits=12, decimal_places=2)
    image = models.CharField("imagem", max_length=255, blank=True)

    class Meta:
        verbose_name = "linha do pedido"
        verbose_name_plural = "linhas dos pedidos"

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
