from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from cart.services import cart_payload
from marketplace_config.api import error, form_error, ok, serialize_order

from .forms import CheckoutForm
from .models import Order
from .services import CheckoutValidationError, create_order


@require_http_methods(["GET", "POST"])
def checkout(request):
    """GET /orders/checkout/ — carrinho e campos do formulário.
    POST /orders/checkout/ — cria o pedido e devolve o passo de pagamento."""
    payload = cart_payload(request)

    accept_header = request.headers.get("Accept", "")
    is_json = (
        request.GET.get("format") == "json"
        or (request.headers.get("x-requested-with") == "XMLHttpRequest" and "text/html" not in accept_header)
        or ("application/json" in accept_header and "text/html" not in accept_header)
    )

    if request.method == "GET":
        initial = {}
        if request.user.is_authenticated:
            initial = {
                "customer_name": request.user.get_full_name() or request.user.username,
                "customer_email": request.user.email,
            }
        form = CheckoutForm(initial=initial)

        if not is_json:
            return render(request, "orders/checkout.html", {"form": form, "cart": payload})

        return ok(
            {
                "cart": payload,
                "fields": [
                    {
                        "name": name,
                        "label": field.label,
                        "required": field.required,
                        "help_text": field.help_text,
                        "initial": initial.get(name, ""),
                    }
                    for name, field in form.fields.items()
                ],
            }
        )

    if not payload["item_count"]:
        return error("O carrinho está vazio.", status=409)

    form = CheckoutForm(request.POST)
    if not form.is_valid():
        return form_error(form)

    try:
        order = create_order(request, form.cleaned_data)
    except CheckoutValidationError as exc:
        return error(str(exc), status=409)

    return ok(
        {
            "order": serialize_order(request, order, detail=True),
            "next": {
                "payment_select": request.build_absolute_uri(
                    f"/payments/order/{order.order_number}/select/"
                )
            },
        },
        status=201,
    )


def _owned_order(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    if order.user_id:
        if not request.user.is_authenticated or order.user_id != request.user.id:
            return None
    elif order.session_key != (request.session.session_key or ""):
        return None
    return order


@require_GET
def success(request, order_number):
    """GET /orders/success/<numero>/ — confirmação do pedido."""
    order = _owned_order(request, order_number)
    if order is None:
        return error("Pedido não encontrado.", status=404)
    return ok({"order": serialize_order(request, order, detail=True)})
