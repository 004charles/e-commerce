from decimal import Decimal, InvalidOperation
from django.db import models
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.urls import reverse
from unicodedata import combining as unicode_combining
from unicodedata import normalize as unicode_normalize
from django.views.decorators.csrf import ensure_csrf_cookie

from catalog.models import Category, Product
from catalog.pricing import price_context
from stores.models import Store

from .models import HomepageBanner, HomepageLink, HomepageTextBlock, SiteSettings


@ensure_csrf_cookie
def home(request):
    context = {
        "featured_products": Product.objects.filter(
            status=Product.Status.ACTIVE,
            featured=True,
            store__status=Store.Status.APPROVED,
        ).select_related("store", "category")[:12],
        "new_products": Product.objects.filter(
            status=Product.Status.ACTIVE,
            store__status=Store.Status.APPROVED,
        ).select_related("store", "category")[:12],
        "featured_categories": Category.objects.filter(is_active=True)[:12],
        "featured_stores": Store.objects.filter(
            status=Store.Status.APPROVED,
            featured=True,
        )[:8],
    }
    return render(request, "homepage/index.html", context)


def home_data(request):
    now = timezone.now()
    banners = HomepageBanner.objects.filter(is_active=True).filter(
        models.Q(starts_at__isnull=True) | models.Q(starts_at__lte=now),
        models.Q(ends_at__isnull=True) | models.Q(ends_at__gt=now),
    )
    products = Product.objects.filter(
        status=Product.Status.ACTIVE,
        stock__gt=0,
        store__status=Store.Status.APPROVED,
    ).select_related("store", "category")[:100]
    payload = {
        "products": [
            {
                "id": product.pk,
                "name": product.name,
                "store": product.store.name,
                "price": f"{price_context(product)['price']:.2f} Kz",
                "compare_at_price": f"{price_context(product)['original_price']:.2f} Kz" if price_context(product)['original_price'] else "",
                "discount_percent": f"{price_context(product)['discount_percent']:.0f}",
                "image": request.build_absolute_uri(product.image.url) if product.image else "",
                "url": request.build_absolute_uri(product.get_absolute_url()),
                "stock": product.stock,
            }
            for product in products
        ],
        "banners": [
            {
                "title": banner.title,
                "button_url": banner.button_url,
                "image": request.build_absolute_uri(banner.image.url) if banner.image else "",
            }
            for banner in banners
        ],
        "categories": [
            {
                "name": category.name,
                "image": request.build_absolute_uri(category.image.url) if category.image else "",
                "url": request.build_absolute_uri(
                    reverse("catalog:category", kwargs={"category_slug": category.slug})
                ),
            }
            for category in Category.objects.filter(is_active=True)[:12]
        ],
        "stores": [
            {"name": store.name, "url": request.build_absolute_uri(store.get_absolute_url())}
            for store in Store.objects.filter(status=Store.Status.APPROVED)[:8]
        ],
        "text_blocks": [
            {
                "key": block.key,
                "title": block.title,
                "subtitle": block.subtitle,
                "body": block.body,
            }
            for block in HomepageTextBlock.objects.filter(is_active=True)
        ],
    }
    return JsonResponse(payload)


def site_data(request):
    now = timezone.now()
    settings = SiteSettings.objects.filter(key="default").first()
    banners = HomepageBanner.objects.filter(is_active=True).filter(
        models.Q(starts_at__isnull=True) | models.Q(starts_at__lte=now),
        models.Q(ends_at__isnull=True) | models.Q(ends_at__gt=now),
    )
    payload = {
        "settings": {
            "site_name": settings.site_name if settings else "Marketplace Angola",
            "tagline": settings.tagline if settings else "",
            "shipping_message": settings.shipping_message if settings else "",
            "support_phone": settings.support_phone if settings else "",
            "support_email": settings.support_email if settings else "",
            "contact_address": settings.contact_address if settings else "",
            "facebook_url": settings.facebook_url if settings else "",
            "instagram_url": settings.instagram_url if settings else "",
            "twitter_url": settings.twitter_url if settings else "",
            "whatsapp_url": settings.whatsapp_url if settings else "",
            "newsletter_title": settings.newsletter_title if settings else "",
            "newsletter_description": settings.newsletter_description if settings else "",
            "currency_code": settings.currency_code if settings else "AOA",
            "currency_symbol": settings.currency_symbol if settings else "Kz",
        },
        "banners": [
            {
                "placement": banner.placement,
                "title": banner.title,
                "subtitle": banner.subtitle,
                "description": banner.description,
                "button_label": banner.button_label,
                "button_url": banner.button_url,
                "image": request.build_absolute_uri(banner.image.url) if banner.image else "",
            }
            for banner in banners
        ],
        "text_blocks": [
            {
                "key": block.key,
                "title": block.title,
                "subtitle": block.subtitle,
                "body": block.body,
                "button_label": block.button_label,
                "button_url": block.button_url,
            }
            for block in HomepageTextBlock.objects.filter(is_active=True)
        ],
        "links": [
            {
                "placement": link.placement,
                "label": link.label,
                "url": link.url,
                "icon": link.icon,
            }
            for link in HomepageLink.objects.filter(is_active=True)
        ],
    }
    return JsonResponse(payload)


def search_data(request):
    query = request.GET.get("q", "").strip()
    store_filter = request.GET.get("store", "").strip()
    province_filter = request.GET.get("province", "").strip()
    min_price = _decimal_filter(request.GET.get("min_price"))
    max_price = _decimal_filter(request.GET.get("max_price"))
    products = list(
        Product.objects.filter(
            status=Product.Status.ACTIVE,
            stock__gt=0,
            store__status=Store.Status.APPROVED,
        ).select_related("store", "category")
    )
    pricing = {product.pk: price_context(product) for product in products}
    normalized_query = _normalize_search(query)
    if normalized_query:
        products = [
            product
            for product in products
            if normalized_query in _normalize_search(
                " ".join(
                    [
                        product.name,
                        product.short_description,
                        product.description,
                        product.store.name,
                        product.store.municipality,
                        product.store.province,
                        product.category.name,
                    ]
                )
            )
        ]
    if store_filter:
        products = [product for product in products if product.store.slug == store_filter]
    if province_filter:
        products = [
            product
            for product in products
            if _normalize_search(product.store.province) == _normalize_search(province_filter)
        ]
    if min_price is not None:
        products = [product for product in products if pricing[product.pk]["price"] >= min_price]
    if max_price is not None:
        products = [product for product in products if pricing[product.pk]["price"] <= max_price]

    products = sorted(products, key=lambda product: (pricing[product.pk]["price"], product.name))[:30]
    results = []
    for product in products:
        results.append(
            {
                "id": product.pk,
                "name": product.name,
                "category": product.category.name,
                "store": product.store.name,
                "store_slug": product.store.slug,
                "province": product.store.province,
                "municipality": product.store.municipality,
                "location": ", ".join(
                    part for part in [product.store.municipality, product.store.province] if part
                ),
                "price": f"{pricing[product.pk]['price']:.2f}",
                "compare_at_price": f"{pricing[product.pk]['original_price']:.2f}" if pricing[product.pk]['original_price'] else "",
                "discount_percent": f"{pricing[product.pk]['discount_percent']:.0f}",
                "image": request.build_absolute_uri(product.image.url) if product.image else "",
                "url": request.build_absolute_uri(product.get_absolute_url()),
                "stock": product.stock,
            }
        )

    offers_by_name = {}
    for product in products:
        comparison_key = _normalize_search(product.name)
        offers_by_name.setdefault(comparison_key, []).append(product)
    comparisons = []
    for comparison_key, offers in offers_by_name.items():
        if len(offers) < 2:
            continue
        ordered_offers = sorted(offers, key=lambda product: pricing[product.pk]["price"])
        comparisons.append(
            {
                "name": ordered_offers[0].name,
                "offers": [
                    {
                        "product_id": offer.pk,
                        "store": offer.store.name,
                        "location": ", ".join(
                            part for part in [offer.store.municipality, offer.store.province] if part
                        ),
                        "price": f"{pricing[offer.pk]['price']:.2f}",
                        "url": request.build_absolute_uri(offer.get_absolute_url()),
                        "is_lowest": offer.pk == ordered_offers[0].pk,
                    }
                    for offer in ordered_offers
                ],
            }
        )
    return JsonResponse(
        {
            "query": query,
            "count": len(results),
            "results": results,
            "comparisons": comparisons,
            "filters": {
                "store": store_filter,
                "province": province_filter,
                "min_price": str(min_price) if min_price is not None else "",
                "max_price": str(max_price) if max_price is not None else "",
            },
            "currency": "AOA",
        }
    )


def _normalize_search(value):
    return "".join(
        character
        for character in unicode_normalize("NFKD", str(value or "").lower())
        if not unicode_combining(character)
    )


def _decimal_filter(value):
    if not value:
        return None
    try:
        return Decimal(value)
    except (InvalidOperation, TypeError, ValueError):
        return None
