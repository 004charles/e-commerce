from django.db import transaction
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render
from django.utils.text import slugify
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from catalog.forms import ProductForm
from catalog.models import Category, Product
from marketplace_config.api import (
    api_login_required,
    error,
    form_error,
    ok,
    serialize_product,
    serialize_store,
)
from orders.models import Order, StoreOrder

from .forms import StoreApplicationForm, StoreOrderStatusForm
from .models import Store


def _vendor_store(user):
    return (
        Store.objects.filter(owner=user, status=Store.Status.APPROVED)
        .select_related("owner")
        .first()
    )


def _require_vendor_store(user):
    store = _vendor_store(user)
    if store is None:
        return None, error(
            "A sua loja precisa de estar aprovada para esta operação.", status=403
        )
    return store, None


def _anonymize_customer(value):
    words = (value or "Cliente").split()
    return " ".join((word[:1] + "***") for word in words[:2])


def _anonymize_phone(value):
    digits = "".join(character for character in (value or "") if character.isdigit())
    return "***" + digits[-2:] if digits else "Não indicado"


@api_login_required
@require_http_methods(["GET", "POST"])
def apply(request):
    """GET  /stores/apply/ — campos da candidatura.
    POST /stores/apply/ — submete a candidatura de vendedor."""
    if request.method == "GET":
        form = StoreApplicationForm()
        return ok(
            {
                "fields": [
                    {
                        "name": name,
                        "label": field.label,
                        "required": field.required,
                        "help_text": field.help_text,
                    }
                    for name, field in form.fields.items()
                ]
            }
        )

    form = StoreApplicationForm(request.POST)
    if not form.is_valid():
        return form_error(form)
    application = form.save(commit=False)
    application.applicant = request.user
    application.save()
    return ok(
        {
            "message": "A sua candidatura foi enviada para análise.",
            "application": {"id": application.pk, "status": application.status},
        },
        status=201,
    )


@api_login_required
@require_GET
def dashboard(request):
    """GET /stores/dashboard/ — painel do vendedor: loja, produtos e pedidos."""
    stores = Store.objects.filter(owner=request.user).prefetch_related("products")
    store = stores.filter(status=Store.Status.APPROVED).first() or stores.first()
    if not store:
        return error("Ainda não tem nenhuma loja.", status=404, has_store=False)

    products = store.products.select_related("category").all()
    store_orders = (
        StoreOrder.objects.filter(store=store)
        .select_related("order")
        .prefetch_related("items")
        .order_by("-created_at")
    )

    return ok(
        {
            "store": serialize_store(request, store, detail=True),
            "stores": [serialize_store(request, s) for s in stores],
            "metrics": {
                "total_products": products.count(),
                "active_products": products.filter(status=Product.Status.ACTIVE).count(),
                "low_stock_products": products.filter(stock__lte=5).count(),
                "orders": store_orders.count(),
            },
            "products": [serialize_product(request, p) for p in products],
            "orders": [
                {
                    "id": store_order.pk,
                    "order_number": store_order.order.order_number,
                    "created_at": store_order.created_at.isoformat(),
                    "status": store_order.status,
                    "status_display": store_order.get_status_display(),
                    "total": str(store_order.total),
                    "customer": _anonymize_customer(store_order.order.customer_name),
                    "phone": _anonymize_phone(store_order.order.customer_phone),
                    "items": [
                        {
                            "product_name": item.product_name,
                            "sku": item.sku,
                            "quantity": item.quantity,
                            "unit_price": str(item.unit_price),
                            "line_total": str(item.line_total),
                        }
                        for item in store_order.items.all()
                    ],
                }
                for store_order in store_orders
            ],
        }
    )


ALLOWED_STATUS_TRANSITIONS = {
    Order.Status.PENDING: {Order.Status.AWAITING_PAYMENT, Order.Status.CANCELLED},
    Order.Status.AWAITING_PAYMENT: {
        Order.Status.PAID,
        Order.Status.PROCESSING,
        Order.Status.CANCELLED,
    },
    Order.Status.PAID: {Order.Status.PROCESSING, Order.Status.CANCELLED},
    Order.Status.PROCESSING: {Order.Status.SHIPPED, Order.Status.CANCELLED},
    Order.Status.SHIPPED: {Order.Status.COMPLETED},
    Order.Status.COMPLETED: set(),
    Order.Status.CANCELLED: set(),
}


@api_login_required
@require_POST
def store_order_status(request, pk):
    """POST /stores/dashboard/orders/<pk>/status/ — muda o estado do pedido."""
    store, failure = _require_vendor_store(request.user)
    if failure:
        return failure

    store_order = get_object_or_404(
        StoreOrder.objects.select_related("order"), pk=pk, store=store
    )
    form = StoreOrderStatusForm(request.POST)
    if not form.is_valid():
        return form_error(form, "Estado de pedido inválido.")

    requested = form.cleaned_data["status"]
    if requested == store_order.status:
        return ok({"message": "O estado já era esse.", "status": store_order.status})
    if requested not in ALLOWED_STATUS_TRANSITIONS.get(store_order.status, set()):
        return error(
            "Esta transição de estado não é permitida.",
            status=409,
            current_status=store_order.status,
            allowed=sorted(ALLOWED_STATUS_TRANSITIONS.get(store_order.status, set())),
        )

    store_order.status = requested
    store_order.save(update_fields=["status", "updated_at"])
    return ok(
        {
            "message": "Estado do pedido atualizado.",
            "status": store_order.status,
            "status_display": store_order.get_status_display(),
        }
    )


@api_login_required
@require_POST
def product_create(request):
    """POST /stores/dashboard/products/new/ — cria um produto na loja."""
    store, failure = _require_vendor_store(request.user)
    if failure:
        return failure

    form = ProductForm(request.POST, request.FILES, store=store)
    if not form.is_valid():
        return form_error(form)

    product = form.save(commit=False)
    product.store = store
    if not product.slug:
        product.slug = slugify(product.name)
    if product.status == Product.Status.ACTIVE and product.stock == 0:
        product.status = Product.Status.OUT_OF_STOCK
    product.save()
    return ok(
        {"message": "Produto criado.", "product": serialize_product(request, product, detail=True)},
        status=201,
    )


@api_login_required
@require_http_methods(["GET", "POST"])
def product_edit(request, pk):
    """GET  /stores/dashboard/products/<pk>/edit/ — dados do produto.
    POST /stores/dashboard/products/<pk>/edit/ — guarda alterações."""
    store, failure = _require_vendor_store(request.user)
    if failure:
        return failure
    product = get_object_or_404(Product, pk=pk, store=store)

    if request.method == "GET":
        return ok({"product": serialize_product(request, product, detail=True)})

    form = ProductForm(request.POST, request.FILES, instance=product, store=store)
    if not form.is_valid():
        return form_error(form)
    product = form.save(commit=False)
    if product.status == Product.Status.ACTIVE and product.stock == 0:
        product.status = Product.Status.OUT_OF_STOCK
    product.save()
    return ok(
        {"message": "Produto atualizado.", "product": serialize_product(request, product, detail=True)}
    )


@api_login_required
@require_POST
def product_delete(request, pk):
    """POST /stores/dashboard/products/<pk>/delete/ — remove o produto."""
    store, failure = _require_vendor_store(request.user)
    if failure:
        return failure
    product = get_object_or_404(Product, pk=pk, store=store)
    product.delete()
    return ok({"message": "Produto removido."})


@api_login_required
@require_POST
def product_stock(request, pk):
    """POST /stores/dashboard/products/<pk>/stock/ — atualiza o stock."""
    store, failure = _require_vendor_store(request.user)
    if failure:
        return failure
    product = get_object_or_404(Product, pk=pk, store=store)

    try:
        stock = int(request.POST.get("stock", ""))
    except (TypeError, ValueError):
        return error("Indique uma quantidade de stock válida.")
    if stock < 0:
        return error("O stock não pode ser negativo.")

    with transaction.atomic():
        product.stock = stock
        if stock == 0 and product.status == Product.Status.ACTIVE:
            product.status = Product.Status.OUT_OF_STOCK
        elif stock > 0 and product.status == Product.Status.OUT_OF_STOCK:
            product.status = Product.Status.DRAFT
        product.save(update_fields=["stock", "status", "updated_at"])

    return ok(
        {
            "message": "Stock atualizado.",
            "stock": product.stock,
            "status": product.status,
        }
    )


@require_GET
def store_list(request):
    """GET /stores/ — lista de lojas públicas aprovadas."""
    stores_qs = (
        Store.objects.filter(status=Store.Status.APPROVED)
        .annotate(
            active_products_count=Count("products", filter=Q(products__status=Product.Status.ACTIVE))
        )
        .order_by("-featured", "name")
    )

    accept_header = request.headers.get("Accept", "")
    is_json = (
        request.GET.get("format") == "json"
        or "application/json" in accept_header
        and "text/html" not in accept_header
    )

    if is_json:
        return ok(
            {
                "count": stores_qs.count(),
                "results": [serialize_store(request, s) for s in stores_qs],
            }
        )

    context = {
        "stores": stores_qs,
        "stores_count": stores_qs.count(),
    }
    return render(request, "stores/store_list.html", context)


@require_GET
def store_detail(request, slug):
    """GET /stores/<slug>/ — perfil público da loja e os seus produtos ativos."""
    store = get_object_or_404(Store, slug=slug, status=Store.Status.APPROVED)
    products_qs = Product.objects.filter(
        store=store, status=Product.Status.ACTIVE
    ).select_related("category", "store")

    total_products_count = products_qs.count()

    category_slug = request.GET.get("category", "").strip()
    if category_slug:
        products_qs = products_qs.filter(category__slug=category_slug)

    sort = request.GET.get("sort", "featured")
    products = list(products_qs)

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
        page_size = min(100, max(1, int(request.GET.get("page_size", 20))))
    except (TypeError, ValueError):
        page, page_size = 1, 20
    start = (page - 1) * page_size
    window = products[start : start + page_size]

    accept_header = request.headers.get("Accept", "")
    is_json = (
        request.GET.get("format") == "json"
        or "application/json" in accept_header
        and "text/html" not in accept_header
    )

    if is_json:
        return ok(
            {
                "store": serialize_store(request, store, detail=True),
                "count": total,
                "products": [serialize_product(request, p) for p in window],
            }
        )

    store_categories = (
        Category.objects.filter(
            products__store=store, products__status=Product.Status.ACTIVE
        )
        .annotate(prod_count=Count("products", filter=Q(products__store=store, products__status=Product.Status.ACTIVE)))
        .filter(prod_count__gt=0)
        .distinct()
    )

    context = {
        "store": store,
        "products": window,
        "total_count": total,
        "total_products_count": total_products_count,
        "store_categories": store_categories,
        "current_category": category_slug,
        "current_sort": sort,
        "page": page,
        "num_pages": (total + page_size - 1) // page_size if total else 0,
    }
    return render(request, "stores/store_detail.html", context)
