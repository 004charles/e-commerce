from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from orders.models import Order


class PaymentProviderConfig(models.Model):
    class Provider(models.TextChoices):
        MULTICAIXA_EXPRESS = "multicaixa_express", "Multicaixa Express"
        UNITEL_MONEY = "unitel_money", "Unitel Money"
        PAYPAY = "paypay", "PayPay"
        KYAMI_PAY = "kyami_pay", "Kyami Pay"

    provider = models.CharField("provedor", max_length=32, choices=Provider.choices, unique=True)
    is_active = models.BooleanField("ativo", default=False)
    is_sandbox = models.BooleanField("modo sandbox", default=True)

    # Credenciais genéricas (campos variam por provedor)
    client_id = models.CharField("Client ID / API Key", max_length=255, blank=True)
    client_secret = models.CharField("Client Secret / Secret Key", max_length=255, blank=True)
    merchant_id = models.CharField("Merchant ID / POS ID", max_length=255, blank=True)
    api_base_url = models.URLField("URL base da API", blank=True)
    webhook_secret = models.CharField("Webhook Secret / HMAC Key", max_length=255, blank=True)

    # Configurações extras em JSON (flexível para cada provedor)
    extra_config = models.JSONField("configuração extra", default=dict, blank=True)

    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        verbose_name = "configuração de provedor de pagamento"
        verbose_name_plural = "configurações de provedores de pagamento"

    def __str__(self):
        return f"{self.get_provider_display()} ({'sandbox' if self.is_sandbox else 'produção'})"


class PaymentAttempt(models.Model):
    class Method(models.TextChoices):
        MULTICAIXA_EXPRESS = "multicaixa_express", "Multicaixa Express"
        UNITEL_MONEY = "unitel_money", "Unitel Money"
        PAYPAY = "paypay", "PayPay"
        KYAMI_PAY = "kyami_pay", "Kyami Pay"

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
