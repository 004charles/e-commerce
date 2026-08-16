from django.db import models

from orders.models import Order


class PaymentAttempt(models.Model):
    class Method(models.TextChoices):
        MULTICAIXA_EXPRESS = "multicaixa_express", "Multicaixa Express"
        UNITEL_MONEY = "unitel_money", "Unitel Money"
        PAYPAY = "paypay", "PayPay"

    class Status(models.TextChoices):
        CREATED = "created", "Criada"
        PENDING = "pending", "Pendente"
        SUCCEEDED = "succeeded", "Concluída"
        FAILED = "failed", "Falhou"
        CANCELLED = "cancelled", "Cancelada"

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="payment_attempts",
        verbose_name="pedido",
    )
    method = models.CharField("método", max_length=32, choices=Method.choices)
    status = models.CharField(
        "estado", max_length=16, choices=Status.choices, default=Status.CREATED
    )
    provider_reference = models.CharField(
        "referência do provedor", max_length=160, blank=True
    )
    message = models.CharField("mensagem", max_length=255, blank=True)
    created_at = models.DateTimeField("criada em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizada em", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "tentativa de pagamento"
        verbose_name_plural = "tentativas de pagamento"

    def __str__(self):
        return f"{self.order.order_number} — {self.get_method_display()} — {self.get_status_display()}"
