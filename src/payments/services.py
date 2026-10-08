from abc import ABC, abstractmethod

from django.db import transaction
from django.conf import settings

from .models import PaymentAttempt, PaymentProviderConfig


class PaymentProvider(ABC):
    method = None

    def __init__(self):
        self.config = self._get_config()

    def _get_config(self):
        try:
            return PaymentProviderConfig.objects.get(provider=self.method, is_active=True)
        except PaymentProviderConfig.DoesNotExist:
            return None

    @abstractmethod
    def start(self, attempt):
        """Inicia uma tentativa através do provedor real quando a integração existir."""
        raise NotImplementedError


class MulticaixaExpressProvider(PaymentProvider):
    method = PaymentAttempt.Method.MULTICAIXA_EXPRESS

    def start(self, attempt):
        return _pending_result(attempt, "Multicaixa Express ainda não está configurado.")


class UnitelMoneyProvider(PaymentProvider):
    method = PaymentAttempt.Method.UNITEL_MONEY

    def start(self, attempt):
        return _pending_result(attempt, "Unitel Money ainda não está configurado.")


class PayPayProvider(PaymentProvider):
    method = PaymentAttempt.Method.PAYPAY

    def start(self, attempt):
        return _pending_result(attempt, "PayPay ainda não está configurado.")


class KyamiPayProvider(PaymentProvider):
    method = PaymentAttempt.Method.KYAMI_PAY

    def start(self, attempt):
        if not self.config:
            return _pending_result(attempt, "Kyami Pay não configurado no admin.")
        
        # TODO: Implementar integração real quando tiver as credenciais
        # Exemplo de como acessar config:
        # self.config.client_id
        # self.config.client_secret
        # self.config.api_base_url
        # self.config.extra_config (dict)
        
        return _pending_result(attempt, "Kyami Pay: aguardando implementação (configure no admin).")


PROVIDERS = {
    PaymentAttempt.Method.MULTICAIXA_EXPRESS: MulticaixaExpressProvider,
    PaymentAttempt.Method.UNITEL_MONEY: UnitelMoneyProvider,
    PaymentAttempt.Method.PAYPAY: PayPayProvider,
    PaymentAttempt.Method.KYAMI_PAY: KyamiPayProvider,
}


def get_provider(method):
    provider_class = PROVIDERS.get(method)
    if not provider_class:
        raise ValueError("Método de pagamento não suportado.")
    return provider_class()


@transaction.atomic
def create_pending_attempt(order, method):
    if method not in PROVIDERS:
        raise ValueError("Método de pagamento não suportado.")
    attempt = PaymentAttempt.objects.create(
        order=order,
        method=method,
        status=PaymentAttempt.Status.PENDING,
        message="Tentativa criada; aguardando configuração do provedor.",
    )
    return get_provider(method).start(attempt)


def _pending_result(attempt, message):
    attempt.status = PaymentAttempt.Status.PENDING
    attempt.message = message
    attempt.save(update_fields=["status", "message", "updated_at"])
    return attempt
