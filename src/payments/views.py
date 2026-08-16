from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PaymentMethodForm
from .models import PaymentAttempt
from .services import create_pending_attempt
from orders.models import Order


def _owned_order(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    if order.user_id:
        if not request.user.is_authenticated or order.user_id != request.user.id:
            return None
    elif order.session_key != (request.session.session_key or ""):
        return None
    return order


def select_payment(request, order_number):
    order = _owned_order(request, order_number)
    if order is None:
        return redirect("/")
    latest_attempt = order.payment_attempts.first()
    if request.method == "POST":
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            attempt = create_pending_attempt(order, form.cleaned_data["method"])
            messages.info(
                request,
                f"{attempt.get_method_display()} foi selecionado. O pagamento permanece pendente até a integração oficial.",
            )
            return redirect("payments:pending", order_number=order.order_number)
    else:
        form = PaymentMethodForm()
    return render(
        request,
        "payments/select.html",
        {"order": order, "form": form, "latest_attempt": latest_attempt},
    )


def pending(request, order_number):
    order = _owned_order(request, order_number)
    if order is None:
        return redirect("/")
    attempt = order.payment_attempts.first()
    return render(request, "payments/pending.html", {"order": order, "attempt": attempt})
