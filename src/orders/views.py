from django.shortcuts import get_object_or_404, redirect, render

from cart.services import cart_payload

from .forms import CheckoutForm
from .models import Order
from .services import CheckoutValidationError, create_order


def checkout(request):
    payload = cart_payload(request)
    if not payload["item_count"]:
        return redirect("/")
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                order = create_order(request, form.cleaned_data)
            except CheckoutValidationError as error:
                form.add_error(None, str(error))
            else:
                return redirect("payments:select", order_number=order.order_number)
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {
                "customer_name": request.user.get_full_name() or request.user.username,
                "customer_email": request.user.email,
            }
        form = CheckoutForm(initial=initial)
    return render(request, "orders/checkout.html", {"form": form, "cart": payload})


def success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    if order.user_id and order.user_id != request.user.id:
        return redirect("/")
    if not order.user_id and order.session_key != (request.session.session_key or ""):
        return redirect("/")
    return render(request, "orders/success.html", {"order": order})
