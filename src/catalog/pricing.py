from decimal import Decimal, ROUND_HALF_UP

from django.utils import timezone

from .models import Product, Promotion


CENT = Decimal("0.01")


def active_promotion(product, now=None):
    now = now or timezone.now()
    promotions = Promotion.objects.filter(
        is_active=True,
        starts_at__lte=now,
        ends_at__gt=now,
    ).filter(product=product)
    category = getattr(product, "category", None)
    if category is not None:
        promotions = Promotion.objects.filter(
            is_active=True,
            starts_at__lte=now,
            ends_at__gt=now,
        ).filter(product=product) | Promotion.objects.filter(
            is_active=True,
            starts_at__lte=now,
            ends_at__gt=now,
            category=category,
        )
    return promotions.order_by("-discount_percent", "-starts_at").first()


def price_context(product, now=None):
    promotion = active_promotion(product, now=now)
    original_price = product.price
    price = product.price
    discount_percent = Decimal("0.00")
    if promotion:
        discount_percent = promotion.discount_percent
        price = (product.price * (Decimal("1.00") - discount_percent / Decimal("100"))).quantize(
            CENT, rounding=ROUND_HALF_UP
        )
    return {
        "price": price,
        "original_price": original_price if promotion else product.compare_at_price,
        "discount_percent": discount_percent,
        "promotion": promotion,
    }


def effective_price(product, now=None):
    return price_context(product, now=now)["price"]
