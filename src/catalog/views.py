from decimal import Decimal, InvalidOperation
from unicodedata import combining, normalize

from django.contrib.auth.decorators import login_required
from django.db import transaction
import json

from django.db.models import Avg, Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from stores.models import Store

from .forms import ReviewForm
from .models import Category, Product, Review
from .pricing import price_context


def product_list(request, category_slug=None):
    products = Product.objects.filter(
        status=Product.Status.ACTIVE,
        store__status=Store.Status.APPROVED,
    ).select_related("store", "category")
    category = None
    query = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "featured")

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug, is_active=True)
        products = products.filter(category=category)
    products = list(products)
    if query:
        normalized_query = _normalize(query)
        products = [
            product
            for product in products
            if normalized_query in _normalize(
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
    store_filter = request.GET.get("store", "").strip()
    province_filter = request.GET.get("province", "").strip()
    min_price = _parse_price(request.GET.get("min_price"))
    max_price = _parse_price(request.GET.get("max_price"))
    if store_filter:
        products = [product for product in products if product.store.slug == store_filter]
    if province_filter:
        products = [
            product
            for product in products
            if _normalize(product.store.province) == _normalize(province_filter)
        ]
    if min_price is not None:
        products = [product for product in products if product.price >= min_price]
    if max_price is not None:
        products = [product for product in products if product.price <= max_price]
    if sort == "price_asc":
        products = sorted(products, key=lambda product: product.price)
    elif sort == "price_desc":
        products = sorted(products, key=lambda product: product.price, reverse=True)
    elif sort == "newest":
        products = sorted(products, key=lambda product: product.created_at, reverse=True)
    else:
        products = sorted(products, key=lambda product: (not product.featured, product.created_at), reverse=True)

    context = {
        "products": products,
        "categories": Category.objects.filter(is_active=True),
        "category": category,
        "query": query,
        "sort": sort,
        "store_filter": store_filter,
        "province_filter": province_filter,
        "min_price": min_price,
        "max_price": max_price,
        "catalog_data": {
            "products": [_catalog_product_payload(request, product) for product in products],
            "category_name": category.name if category else "Catálogo",
            "category_url": request.build_absolute_uri(reverse("catalog:category", kwargs={"category_slug": category.slug})) if category else request.build_absolute_uri("/catalog/"),
            "categories": [
                {
                    "name": item.name,
                    "url": request.build_absolute_uri(reverse("catalog:category", kwargs={"category_slug": item.slug})),
                    "count": item.products.filter(
                        status=Product.Status.ACTIVE,
                        store__status=Store.Status.APPROVED,
                    ).count(),
                }
                for item in Category.objects.filter(is_active=True)
            ],
        },
    }
    return render(request, "catalog/list.html", context)



def _catalog_product_payload(request, product):
    pricing = price_context(product)
    return {
        "id": product.pk,
        "name": product.name,
        "store": product.store.name,
        "price": f"{pricing['price']:.2f} Kz",
        "compare_at_price": f"{pricing['original_price']:.2f} Kz" if pricing["original_price"] else "",
        "discount_percent": f"{pricing['discount_percent']:.0f}",
        "image": request.build_absolute_uri(product.image.url) if product.image else "",
        "url": request.build_absolute_uri(product.get_absolute_url()),
        "stock": product.stock,
        "rating": float(product.rating or 0),
    }


def _normalize(value):
    return "".join(character for character in normalize("NFKD", str(value or "").lower()) if not combining(character))


def _parse_price(value):
    if not value:
        return None
    try:
        return Decimal(value)
    except (InvalidOperation, TypeError, ValueError):
        return None


def legacy_product_detail(request, store_slug, slug):
    return redirect("catalog:detail", store_slug=store_slug, slug=slug, permanent=True)


@ensure_csrf_cookie
def product_detail(request, store_slug, slug):
    product = get_object_or_404(
        Product.objects.select_related("store", "category"),
        store__slug=store_slug,
        slug=slug,
        status=Product.Status.ACTIVE,
        store__status=Store.Status.APPROVED,
    )
    pricing = price_context(product)
    reviews = product.reviews.select_related("user").all()
    aggregate = reviews.aggregate(rating=Avg("rating"), review_count=Count("id"))
    review_count = aggregate["review_count"] or product.review_count
    review_rating = aggregate["rating"] if aggregate["review_count"] else product.rating
    canonical_url = request.build_absolute_uri(product.get_absolute_url())
    seo_description = (product.short_description or product.description or f"{product.name} disponível em {product.store.name}.").strip()[:160]
    image_url = request.build_absolute_uri(product.image.url) if product.image else request.build_absolute_uri("/assets/images/product/146.png")
    structured_data = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": product.name,
        "description": seo_description,
        "image": [image_url],
        "sku": product.sku,
        "brand": {"@type": "Brand", "name": product.store.name},
        "category": product.category.name,
        "url": canonical_url,
        "offers": {
            "@type": "Offer",
            "url": canonical_url,
            "priceCurrency": "AOA",
            "price": str(pricing["price"]),
            "availability": "https://schema.org/InStock" if product.is_available else "https://schema.org/OutOfStock",
            "seller": {"@type": "Organization", "name": product.store.name},
        },
    }
    if review_count:
        structured_data["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": str(review_rating),
            "reviewCount": review_count,
        }
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
    purchased = _has_eligible_purchase(product, request.user)
    context = {
        "product": product,
        "pricing": pricing,
        "canonical_url": canonical_url,
        "seo_description": seo_description,
        "structured_data": mark_safe(json.dumps(structured_data, ensure_ascii=False).replace("<", "\\u003c")),
        "reviews": reviews,
        "review_form": ReviewForm(),
        "user_review": user_review,
        "can_review": request.user.is_authenticated and purchased and user_review is None,
        "rating_distribution": _rating_distribution(reviews),
        "reviews_payload": [
            {
                "name": review.user.get_full_name() or review.user.username,
                "rating": review.rating,
                "comment": review.comment,
                "created_at": review.created_at.strftime("%d/%m/%Y"),
            }
            for review in reviews
        ],
        "review_context": {
            "rating": float(review_rating or 0),
            "review_count": review_count,
            "rating_distribution": _rating_distribution(reviews),
            "reviews": [
                {
                    "name": review.user.get_full_name() or review.user.username,
                    "rating": review.rating,
                    "comment": review.comment,
                    "created_at": review.created_at.strftime("%d/%m/%Y"),
                }
                for review in reviews
            ],
            "authenticated": request.user.is_authenticated,
            "can_review": request.user.is_authenticated and purchased and user_review is None,
            "has_review": user_review is not None,
            "submit_url": f"/catalog/product/{product.store.slug}/{product.slug}/review/",
        },
    }
    return render(request, "catalog/detail.html", context)


@login_required(login_url="/account/login/")
@require_POST
def submit_review(request, store_slug, slug):
    product = get_object_or_404(
        Product,
        store__slug=store_slug,
        slug=slug,
        status=Product.Status.ACTIVE,
        store__status=Store.Status.APPROVED,
    )
    if not _has_eligible_purchase(product, request.user):
        return _review_response(request, "Só podes avaliar produtos que compraste após o pagamento ou envio do pedido.", status=403)
    if Review.objects.filter(product=product, user=request.user).exists():
        return _review_response(request, "Já avaliaste este produto.", status=409)

    form = ReviewForm(request.POST)
    if not form.is_valid():
        return _review_response(request, "Verifica a classificação e o comentário enviados.", errors=form.errors, status=400)

    with transaction.atomic():
        review = form.save(commit=False)
        review.product = Product.objects.select_for_update().get(pk=product.pk)
        review.user = request.user
        review.save()
        aggregate = Review.objects.filter(product=review.product).aggregate(
            rating=Avg("rating"), review_count=Count("id")
        )
        review.product.rating = aggregate["rating"] or 0
        review.product.review_count = aggregate["review_count"] or 0
        review.product.save(update_fields=["rating", "review_count", "updated_at"])

    return _review_response(request, "A tua avaliação foi publicada.", success=True)


def _has_eligible_purchase(product, user):
    if not user or not user.is_authenticated:
        return False
    from orders.models import Order

    return product.order_items.filter(
        store_order__order__user=user,
    ).filter(
        store_order__status__in=[
            Order.Status.PAID,
            Order.Status.PROCESSING,
            Order.Status.SHIPPED,
            Order.Status.COMPLETED,
        ]
    ).exists() or product.order_items.filter(
        store_order__order__user=user,
        store_order__order__payment_status=Order.PaymentStatus.PAID,
    ).exists()


def _rating_distribution(reviews):
    total = reviews.count()
    counts = {rating: 0 for rating in range(1, 6)}
    for row in reviews.values("rating").annotate(total=Count("id")):
        counts[row["rating"]] = row["total"]
    return {
        rating: {
            "count": counts[rating],
            "percent": round((counts[rating] / total) * 100) if total else 0,
        }
        for rating in range(5, 0, -1)
    }


def _review_response(request, message, success=False, errors=None, status=200):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        payload = {"success": success, "message": message}
        if errors:
            payload["errors"] = errors.get_json_data()
        return JsonResponse(payload, status=status)
    from django.contrib import messages

    (messages.success if success else messages.error)(request, message)
    return redirect(request.META.get("HTTP_REFERER") or "/")
