from collections import defaultdict
from decimal import Decimal

from django.db import transaction
from django.utils.crypto import get_random_string

from cart.models import Cart
from catalog.models import Product
from catalog.pricing import effective_price

from .models import Order, OrderItem, StoreOrder


class CheckoutValidationError(Exception):
    pass


def get_order_cart(request):
    if not request.session.session_key:
        request.session.create()
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        Cart.objects.filter(session_key=request.session.session_key, user__isnull=True).exclude(pk=cart.pk).delete()
        return cart
    cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key, user__isnull=True)
    return cart


def _order_number():
    return "MA-" + get_random_string(12, "ABCDEFGHJKLMNPQRSTUVWXYZ23456789")


def _revalidate_cart(cart):
    items = list(cart.items.select_related("product__store").select_for_update())
    if not items:
        raise CheckoutValidationError("O carrinho está vazio.")
    grouped = defaultdict(list)
    for item in items:
        product = item.product
        if not product.is_available or product.store.status != product.store.Status.APPROVED:
            raise CheckoutValidationError(f"O produto {product.name} já não está disponível.")
        if item.quantity > product.stock:
            raise CheckoutValidationError(f"O stock de {product.name} foi alterado. Atualize o carrinho.")
        grouped[product.store_id].append(item)
    return items, grouped


@transaction.atomic
def create_order(request, cleaned_data):
    cart = get_order_cart(request)
    items, grouped = _revalidate_cart(cart)
    product_ids = [item.product_id for item in items]
    locked_products = {
        product.pk: product
        for product in Product.objects.select_for_update().select_related("store").filter(pk__in=product_ids)
    }
    subtotal = Decimal("0.00")
    store_subtotals = {}
    for store_id, store_items in grouped.items():
        store_subtotal = Decimal("0.00")
        for cart_item in store_items:
            product = locked_products[cart_item.product_id]
            if cart_item.quantity > product.stock or not product.is_available:
                raise CheckoutValidationError(f"O stock de {product.name} foi alterado. Atualize o carrinho.")
            store_subtotal += effective_price(product) * cart_item.quantity
        store_subtotals[store_id] = store_subtotal
        subtotal += store_subtotal

    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        session_key=request.session.session_key or "",
        order_number=_order_number(),
        subtotal=subtotal,
        shipping_total=Decimal("0.00"),
        total=subtotal,
        currency="AOA",
        status=Order.Status.AWAITING_PAYMENT,
        payment_status=Order.PaymentStatus.NOT_STARTED,
        **cleaned_data,
    )
    for store_id, store_items in grouped.items():
        store = store_items[0].product.store
        store_order = StoreOrder.objects.create(
            order=order,
            store=store,
            subtotal=store_subtotals[store_id],
            shipping_total=Decimal("0.00"),
            total=store_subtotals[store_id],
            status=Order.Status.AWAITING_PAYMENT,
        )
        for cart_item in store_items:
            product = locked_products[cart_item.product_id]
            unit_price = effective_price(product)
            line_total = unit_price * cart_item.quantity
            OrderItem.objects.create(
                store_order=store_order,
                product=product,
                product_name=product.name,
                sku=product.sku,
                store_name=product.store.name,
                unit_price=unit_price,
                quantity=cart_item.quantity,
                line_total=line_total,
                image=product.image.name if product.image else "",
            )
            product.stock -= cart_item.quantity
            if product.stock == 0:
                product.status = Product.Status.OUT_OF_STOCK
                product.save(update_fields=["stock", "status", "updated_at"])
            else:
                product.save(update_fields=["stock", "updated_at"])
    cart.items.all().delete()
    cart.save(update_fields=["updated_at"])
    return order
