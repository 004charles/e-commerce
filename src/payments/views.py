from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET, require_http_methods

from marketplace_config.api import error, form_error, ok, serialize_order
from orders.models import Order

from .forms import PaymentMethodForm
from .services import create_pending_attempt


def _owned_order(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    if order.user_id:
        if not request.user.is_authenticated or order.user_id != request.user.id:
            return None
    elif order.session_key != (request.session.session_key or ""):
        return None
    return order


def _serialize_attempt(attempt):
    if attempt is None:
        return None
    return {
        "method": attempt.method,
        "method_display": attempt.get_method_display(),
        "status": attempt.status,
        "status_display": attempt.get_status_display(),
        "message": attempt.message,
        "created_at": attempt.created_at.isoformat(),
    }


@require_http_methods(["GET", "POST"])
def select_payment(request, order_number):
    """GET  /payments/order/<numero>/select/ — métodos disponíveis.
    POST /payments/order/<numero>/select/ — regista a escolha."""
    order = _owned_order(request, order_number)
    if order is None:
        return error("Pedido não encontrado.", status=404)

    if request.method == "GET":
        form = PaymentMethodForm()
        return ok(
            {
                "order": serialize_order(request, order),
                "methods": [
                    {"value": value, "label": label}
                    for value, label in form.fields["method"].choices
                ],
                "latest_attempt": _serialize_attempt(order.payment_attempts.first()),
            }
        )

    form = PaymentMethodForm(request.POST)
    if not form.is_valid():
        return form_error(form, "Método de pagamento inválido.")

    attempt = create_pending_attempt(order, form.cleaned_data["method"])
    return ok(
        {
            "order": serialize_order(request, order),
            "attempt": _serialize_attempt(attempt),
            "message": (
                f"{attempt.get_method_display()} foi selecionado. "
                "O pagamento permanece pendente até à confirmação."
            ),
            "next": {
                "payment_pending": request.build_absolute_uri(
                    f"/payments/order/{order.order_number}/pending/"
                )
            },
        },
        status=201,
    )


@require_GET
def pending(request, order_number):
    """GET /payments/order/<numero>/pending/ — estado do pagamento."""
    order = _owned_order(request, order_number)
    if order is None:
        return error("Pedido não encontrado.", status=404)
    return ok(
        {
            "order": serialize_order(request, order),
            "attempt": _serialize_attempt(order.payment_attempts.first()),
        }
    )
