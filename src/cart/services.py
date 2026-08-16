from django.db import transaction

from catalog.models import Product
from catalog.pricing import price_context
from stores.models import Store

from .models import Cart, CartItem


class CartValidationError(Exception):
    """Erro de negócio ao validar um carrinho ou a quantidade pedida."""


def get_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart

    if not request.session.session_key:
        request.session.create()
    cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


def get_cart_with_items(request):
    cart = get_cart(request)
    return Cart.objects.prefetch_related(
        "items__product__store",
        "items__product__category",
    ).get(pk=cart.pk)


def _available_product(product_id):
    product = Product.objects.select_for_update().select_related("store").filter(
        pk=product_id,
        status=Product.Status.ACTIVE,
        store__status=Store.Status.APPROVED,
    ).first()
    if not product:
        raise CartValidationError("Este produto já não está disponível.")
    if product.stock <= 0:
        raise CartValidationError("Este produto está sem stock.")
    return product


def add_item(request, product_id, quantity=1):
    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        raise CartValidationError("A quantidade indicada não é válida.")
    if quantity < 1:
        raise CartValidationError("A quantidade deve ser pelo menos 1.")

    with transaction.atomic():
        cart = get_cart(request)
        product = _available_product(product_id)
        if quantity > product.stock:
            raise CartValidationError("A quantidade pedida ultrapassa o stock disponível.")
        item, created = CartItem.objects.select_for_update().get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity},
        )
        if not created:
            new_quantity = item.quantity + quantity
            if new_quantity > product.stock:
                raise CartValidationError("A quantidade pedida ultrapassa o stock disponível.")
            item.quantity = new_quantity
            item.save(update_fields=["quantity", "updated_at"])
        cart.save(update_fields=["updated_at"])
    return item


def update_item(request, product_id, quantity):
    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        raise CartValidationError("A quantidade indicada não é válida.")
    if quantity < 1:
        return remove_item(request, product_id)

    with transaction.atomic():
        cart = get_cart(request)
        product = _available_product(product_id)
        item = CartItem.objects.select_for_update().filter(cart=cart, product=product).first()
        if not item:
            raise CartValidationError("Este produto não está no seu carrinho.")
        if quantity > product.stock:
            raise CartValidationError("A quantidade pedida ultrapassa o stock disponível.")
        item.quantity = quantity
        item.save(update_fields=["quantity", "updated_at"])
        cart.save(update_fields=["updated_at"])
    return item


def remove_item(request, product_id):
    cart = get_cart(request)
    deleted, _ = CartItem.objects.filter(cart=cart, product_id=product_id).delete()
    if not deleted:
        raise CartValidationError("Este produto não está no seu carrinho.")
    cart.save(update_fields=["updated_at"])


def cart_payload(request):
    cart = get_cart_with_items(request)
    groups = []
    for store, items in cart.grouped_by_store().items():
        groups.append(
            {
                "store_id": store.pk,
                "store_name": store.name,
                "items": [
                    {
                        "product_id": item.product_id,
                        "name": item.product.name,
                        "url": item.product.get_absolute_url(),
                        "image": item.product.image.url if item.product.image else "",
                        "price": f"{price_context(item.product)['price']:.2f}",
                        "original_price": f"{price_context(item.product)['original_price']:.2f}" if price_context(item.product)["original_price"] else "",
                        "discount_percent": f"{price_context(item.product)['discount_percent']:.0f}",
                        "quantity": item.quantity,
                        "stock": item.product.stock,
                        "line_total": f"{item.line_total:.2f}",
                    }
                    for item in items
                ],
            }
        )
    return {
        "cart_id": cart.pk,
        "groups": groups,
        "item_count": cart.total_quantity,
        "subtotal": f"{cart.subtotal:.2f}",
        "currency": "AOA",
    }
