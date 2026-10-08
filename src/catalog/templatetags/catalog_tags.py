from django import template
from decimal import Decimal
from catalog.pricing import price_context

register = template.Library()


@register.filter
def currency(value, symbol="Kz"):
    if value is None or value == "":
        return ""
    try:
        val = Decimal(str(value))
        return f"{val:,.2f} {symbol}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return f"{value} {symbol}"


@register.filter
def get_effective_price(product):
    try:
        ctx = price_context(product)
        return ctx["price"]
    except Exception:
        return product.price


@register.filter
def get_discount_percent(product):
    try:
        if product.compare_at_price and product.compare_at_price > product.price:
            diff = ((product.compare_at_price - product.price) / product.compare_at_price) * 100
            return int(round(diff))
        ctx = price_context(product)
        if ctx.get("discount_percent"):
            return int(round(ctx["discount_percent"]))
    except Exception:
        pass
    return 0


@register.filter
def get_original_price(product):
    try:
        if product.compare_at_price and product.compare_at_price > product.price:
            return product.compare_at_price
        ctx = price_context(product)
        return ctx.get("original_price")
    except Exception:
        return None
