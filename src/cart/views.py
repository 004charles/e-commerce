from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_GET, require_POST

from .services import (
    CartValidationError,
    add_item as add_cart_item,
    cart_payload,
    remove_item as remove_cart_item,
    update_item as update_cart_item,
)


def _error(message, status=400):
    return JsonResponse({"ok": False, "error": message}, status=status)


def legacy_cart_page(request):
    return redirect("/?open_cart=1")


@require_GET
def summary(request):
    return JsonResponse({"ok": True, "cart": cart_payload(request)})


@require_POST
def add_item(request):
    try:
        product_id = int(request.POST.get("product_id", ""))
        quantity = request.POST.get("quantity", "1")
        add_cart_item(request, product_id, quantity)
    except (TypeError, ValueError):
        return _error("O produto indicado não é válido.")
    except CartValidationError as error:
        return _error(str(error))
    return JsonResponse({"ok": True, "cart": cart_payload(request)})


@require_POST
def update_item(request):
    try:
        product_id = int(request.POST.get("product_id", ""))
        quantity = request.POST.get("quantity", "1")
        update_cart_item(request, product_id, quantity)
    except (TypeError, ValueError):
        return _error("O produto indicado não é válido.")
    except CartValidationError as error:
        return _error(str(error))
    return JsonResponse({"ok": True, "cart": cart_payload(request)})


@require_POST
def remove_item(request):
    try:
        product_id = int(request.POST.get("product_id", ""))
        remove_cart_item(request, product_id)
    except (TypeError, ValueError):
        return _error("O produto indicado não é válido.")
    except CartValidationError as error:
        return _error(str(error))
    return JsonResponse({"ok": True, "cart": cart_payload(request)})
