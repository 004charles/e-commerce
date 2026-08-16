from abc import ABC, abstractmethod

from django.db import transaction

from .models import PaymentAttempt


class PaymentProvider(ABC):
    method = None

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


PROVIDERS = {
    PaymentAttempt.Method.MULTICAIXA_EXPRESS: MulticaixaExpressProvider,
    PaymentAttempt.Method.UNITEL_MONEY: UnitelMoneyProvider,
    PaymentAttempt.Method.PAYPAY: PayPayProvider,
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
