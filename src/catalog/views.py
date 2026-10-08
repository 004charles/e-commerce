import json
from decimal import Decimal, InvalidOperation
from unicodedata import combining, normalize

from django.db import transaction
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from marketplace_config.api import (
    api_login_required,
    error,
    form_error,
    ok,
    serialize_category,
    serialize_product,
)
from stores.models import Store

from .forms import ReviewForm
from .models import Category, Product, Review
from .pricing import price_context


def _normalize(value):
    return "".join(
        character
        for character in normalize("NFKD", str(value or "").lower())
        if not combining(character)
    )


def _parse_price(value):
    if not value:
        return None
    try:
        return Decimal(value)
    except (InvalidOperation, TypeError, ValueError):
        return None


@require_GET
def product_list(request, category_slug=None):
    """GET /catalog/ — lista de produtos com filtros, ordenação e paginação."""
    products = Product.objects.filter(
        status=Product.Status.ACTIVE,
        store__status=Store.Status.APPROVED,
    ).select_related("store", "category")

    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug, is_active=True)
        products = products.filter(category=category)

    query = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "featured")
    store_filter = request.GET.get("store", "").strip()
    province_filter = request.GET.get("province", "").strip()
    min_price = _parse_price(request.GET.get("min_price"))
    max_price = _parse_price(request.GET.get("max_price"))

    if store_filter:
        products = products.filter(store__slug=store_filter)
    if min_price is not None:
        products = products.filter(price__gte=min_price)
    if max_price is not None:
        products = products.filter(price__lte=max_price)

    products = list(products)

    if query:
        needle = _normalize(query)
        products = [
            product
            for product in products
            if needle
            in _normalize(
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
    if province_filter:
        needle = _normalize(province_filter)
        products = [p for p in products if _normalize(p.store.province) == needle]

    if sort == "price_asc":
        products.sort(key=lambda p: p.price)
    elif sort == "price_desc":
        products.sort(key=lambda p: p.price, reverse=True)
    elif sort == "newest":
        products.sort(key=lambda p: p.created_at, reverse=True)
    elif sort == "rating":
        products.sort(key=lambda p: (p.rating, p.review_count), reverse=True)
    else:
        products.sort(key=lambda p: (not p.featured, p.created_at), reverse=True)

    total = len(products)
    try:
        page = max(1, int(request.GET.get("page", 1)))
        page_size = min(100, max(1, int(request.GET.get("page_size", 24))))
    except (TypeError, ValueError):
        page, page_size = 1, 24
    start = (page - 1) * page_size
    window = products[start : start + page_size]

    accept_header = request.headers.get("Accept", "")
    is_json = (
        request.GET.get("format") == "json"
        or (request.headers.get("x-requested-with") == "XMLHttpRequest" and "text/html" not in accept_header)
        or ("application/json" in accept_header and "text/html" not in accept_header)
    )

    if is_json:
        return ok(
            {
                "count": total,
                "page": page,
                "page_size": page_size,
                "num_pages": (total + page_size - 1) // page_size if total else 0,
                "category": serialize_category(request, category) if category else None,
                "filters": {
                    "q": query,
                    "sort": sort,
                    "store": store_filter,
                    "province": province_filter,
                    "min_price": str(min_price) if min_price is not None else None,
                    "max_price": str(max_price) if max_price is not None else None,
                },
                "results": [serialize_product(request, product) for product in window],
            }
        )

    context = {
        "products": window,
        "total_count": total,
        "page": page,
        "num_pages": (total + page_size - 1) // page_size if total else 0,
        "current_category": category,
        "categories": Category.objects.filter(is_active=True),
        "stores": Store.objects.filter(status=Store.Status.APPROVED),
        "filters": {
            "q": query,
            "sort": sort,
            "store": store_filter,
            "province": province_filter,
            "min_price": str(min_price) if min_price is not None else "",
            "max_price": str(max_price) if max_price is not None else "",
        },
    }
    return render(request, "catalog/shop_grid.html", context)


@require_GET
def category_list(request):
    """GET /catalog/categories/ — categorias ativas e respetiva contagem."""
    categories = Category.objects.filter(is_active=True)
    return ok(
        {
            "results": [
                dict(
                    serialize_category(request, category),
                    product_count=category.products.filter(
                        status=Product.Status.ACTIVE,
                        store__status=Store.Status.APPROVED,
                    ).count(),
                )
                for category in categories
            ]
        }
    )


def legacy_product_detail(request, store_slug, slug):
    return redirect("catalog:detail", store_slug=store_slug, slug=slug, permanent=True)


def _get_active_product(store_slug, slug):
    return get_object_or_404(
        Product.objects.select_related("store", "category"),
        store__slug=store_slug,
        slug=slug,
        status=Product.Status.ACTIVE,
        store__status=Store.Status.APPROVED,
    )


@require_GET
def product_detail(request, store_slug, slug):
    """GET /catalog/product/<loja>/<produto>/ — detalhe, avaliações e JSON-LD."""
    product = _get_active_product(store_slug, slug)
    pricing = price_context(product)
    reviews = product.reviews.select_related("user").all()
    aggregate = reviews.aggregate(rating=Avg("rating"), review_count=Count("id"))
    review_count = aggregate["review_count"] or product.review_count
    review_rating = aggregate["rating"] if aggregate["review_count"] else product.rating

    canonical_url = request.build_absolute_uri(product.get_absolute_url())
    seo_description = (
        product.short_description
        or product.description
        or f"{product.name} disponível em {product.store.name}."
    ).strip()[:160]
    image_url = request.build_absolute_uri(product.image.url) if product.image else ""

    structured_data = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": product.name,
        "description": seo_description,
        "image": [image_url] if image_url else [],
        "sku": product.sku,
        "brand": {"@type": "Brand", "name": product.store.name},
        "category": product.category.name,
        "url": canonical_url,
        "offers": {
            "@type": "Offer",
            "url": canonical_url,
            "priceCurrency": "AOA",
            "price": str(pricing["price"]),
            "availability": "https://schema.org/InStock"
            if product.is_available
            else "https://schema.org/OutOfStock",
            "seller": {"@type": "Organization", "name": product.store.name},
        },
    }
    if review_count:
        structured_data["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": str(review_rating),
            "reviewCount": review_count,
        }

    user_review = (
        reviews.filter(user=request.user).first() if request.user.is_authenticated else None
    )
    purchased = _has_eligible_purchase(product, request.user)

    accept_header = request.headers.get("Accept", "")
    is_json = (
        request.GET.get("format") == "json"
        or (request.headers.get("x-requested-with") == "XMLHttpRequest" and "text/html" not in accept_header)
        or ("application/json" in accept_header and "text/html" not in accept_header)
    )

    if not is_json:
        context = {
            "product": product,
            "pricing": pricing,
            "reviews": reviews,
            "review_count": review_count,
            "review_rating": review_rating,
            "can_review": request.user.is_authenticated and purchased and user_review is None,
            "has_review": user_review is not None,
            "user_review": user_review,
        }
        return render(request, "catalog/detail.html", context)

    return ok(
        {
            "product": serialize_product(request, product, detail=True),
            "seo": {
                "canonical_url": canonical_url,
                "description": seo_description,
                "structured_data": structured_data,
            },
            "reviews": {
                "rating": float(review_rating or 0),
                "count": review_count,
                "distribution": _rating_distribution(reviews),
                "can_review": request.user.is_authenticated and purchased and user_review is None,
                "has_review": user_review is not None,
                "submit_url": request.build_absolute_uri(
                    f"/catalog/product/{product.store.slug}/{product.slug}/review/"
                ),
                "results": [
                    {
                        "name": review.user.get_full_name() or review.user.username,
                        "rating": review.rating,
                        "comment": review.comment,
                        "created_at": review.created_at.isoformat(),
                    }
                    for review in reviews
                ],
            },
        }
    )


@api_login_required
@require_POST
def submit_review(request, store_slug, slug):
    """POST /catalog/product/<loja>/<produto>/review/ — publicar avaliação."""
    product = _get_active_product(store_slug, slug)

    if not _has_eligible_purchase(product, request.user):
        return error(
            "Só pode avaliar produtos que comprou, após o pagamento ou envio do pedido.",
            status=403,
        )
    if Review.objects.filter(product=product, user=request.user).exists():
        return error("Já avaliou este produto.", status=409)

    form = ReviewForm(request.POST)
    if not form.is_valid():
        return form_error(form, "Verifique a classificação e o comentário enviados.")

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

    return ok(
        {
            "message": "A sua avaliação foi publicada.",
            "review": {
                "rating": review.rating,
                "comment": review.comment,
                "created_at": review.created_at.isoformat(),
            },
        },
        status=201,
    )


def _has_eligible_purchase(product, user):
    if not user or not user.is_authenticated:
        return False
    from orders.models import Order

    return (
        product.order_items.filter(store_order__order__user=user)
        .filter(
            store_order__status__in=[
                Order.Status.PAID,
                Order.Status.PROCESSING,
                Order.Status.SHIPPED,
                Order.Status.COMPLETED,
            ]
        )
        .exists()
        or product.order_items.filter(
            store_order__order__user=user,
            store_order__order__payment_status=Order.PaymentStatus.PAID,
        ).exists()
    )


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
