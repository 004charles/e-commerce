"""Helpers partilhados pela API JSON.

O projeto não serve HTML: todas as views públicas devolvem JSON e a única
interface renderizada é o Django admin.
"""

from django.conf import settings
from django.http import JsonResponse


def ok(data=None, status=200, **extra):
    payload = {"ok": True}
    if data is not None:
        payload.update(data)
    payload.update(extra)
    return JsonResponse(payload, status=status)


def error(message, status=400, **extra):
    payload = {"ok": False, "error": message}
    payload.update(extra)
    return JsonResponse(payload, status=status)


def form_error(form, message="Verifique os dados introduzidos.", status=400):
    return JsonResponse(
        {"ok": False, "error": message, "errors": form.errors.get_json_data()},
        status=status,
    )


def absolute(request, url):
    return request.build_absolute_uri(url) if url else ""


# --- serializadores -------------------------------------------------------


def serialize_product(request, product, detail=False):
    from catalog.pricing import price_context

    pricing = price_context(product)
    data = {
        "id": product.pk,
        "name": product.name,
        "slug": product.slug,
        "sku": product.sku,
        "url": absolute(request, product.get_absolute_url()),
        "image": absolute(request, product.image.url) if product.image else "",
        "price": str(pricing["price"]),
        "original_price": str(pricing["original_price"]) if pricing["original_price"] else None,
        "discount_percent": round(float(pricing["discount_percent"] or 0)),
        "currency": "AOA",
        "stock": product.stock,
        "in_stock": product.stock > 0,
        "status": product.status,
        "featured": product.featured,
        "is_new": product.is_new,
        "rating": float(product.rating or 0),
        "review_count": product.review_count,
        "store": {
            "id": product.store_id,
            "name": product.store.name,
            "slug": product.store.slug,
        },
        "category": {
            "id": product.category_id,
            "name": product.category.name,
            "slug": product.category.slug,
        },
        "short_description": product.short_description,
    }
    if detail:
        data["description"] = product.description
        data["created_at"] = product.created_at.isoformat()
        data["updated_at"] = product.updated_at.isoformat()
    return data


def serialize_category(request, category):
    return {
        "id": category.pk,
        "name": category.name,
        "slug": category.slug,
        "image": absolute(request, category.image.url) if category.image else "",
        "sort_order": category.sort_order,
    }


def serialize_store(request, store, detail=False):
    data = {
        "id": store.pk,
        "name": store.name,
        "slug": store.slug,
        "status": store.status,
        "province": store.province,
        "municipality": store.municipality,
    }
    if detail:
        data["description"] = getattr(store, "description", "")
        data["featured"] = getattr(store, "featured", False)
    return data


def serialize_order(request, order, detail=False):
    data = {
        "order_number": order.order_number,
        "created_at": order.created_at.isoformat(),
        "status": order.status,
        "status_display": order.get_status_display(),
        "payment_status": order.payment_status,
        "payment_status_display": order.get_payment_status_display(),
        "payment_method": order.payment_method,
        "subtotal": str(order.subtotal),
        "shipping_total": str(order.shipping_total),
        "total": str(order.total),
        "currency": order.currency,
    }
    if detail:
        data["customer"] = {
            "name": order.customer_name,
            "email": order.customer_email,
            "phone": order.customer_phone,
        }
        data["shipping"] = {
            "province": order.province,
            "municipality": order.municipality,
            "address": order.address,
            "address_details": order.address_details,
            "notes": order.notes,
        }
        data["stores"] = [
            {
                "store": serialize_store(request, store_order.store),
                "status": store_order.status,
                "status_display": store_order.get_status_display(),
                "subtotal": str(store_order.subtotal),
                "shipping_total": str(store_order.shipping_total),
                "total": str(store_order.total),
                "items": [
                    {
                        "product_id": item.product_id,
                        "product_name": item.product_name,
                        "sku": item.sku,
                        "quantity": item.quantity,
                        "unit_price": str(item.unit_price),
                        "line_total": str(item.line_total),
                        # OrderItem.image é um CharField com o caminho em MEDIA_ROOT
                        "image": absolute(request, settings.MEDIA_URL + item.image) if item.image else "",
                    }
                    for item in store_order.items.all()
                ],
            }
            for store_order in order.store_orders.all()
        ]
    return data


def serialize_user(user):
    return {
        "id": user.pk,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "full_name": user.get_full_name(),
        "phone": user.phone,
        "role": user.role,
    }


def api_login_required(view):
    """Como o login_required, mas devolve 401 JSON em vez de redirecionar."""
    from functools import wraps

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return error("Autenticação necessária.", status=401)
        return view(request, *args, **kwargs)

    return wrapper
