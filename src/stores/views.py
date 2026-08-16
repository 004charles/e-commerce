from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import slugify
from django.views.decorators.http import require_POST

from catalog.forms import ProductForm
from catalog.models import Product
from orders.models import Order, StoreOrder

from .forms import StoreApplicationForm, StoreOrderStatusForm
from .models import Store


def _vendor_store(user):
    return (
        Store.objects.filter(owner=user, status=Store.Status.APPROVED)
        .select_related("owner")
        .first()
    )


@login_required
def apply(request):
    form = StoreApplicationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        application = form.save(commit=False)
        application.applicant = request.user
        application.save()
        messages.success(request, "A sua candidatura foi enviada para análise.")
        return redirect("stores:application-success")
    return render(request, "stores/apply.html", {"form": form})


def application_success(request):
    return render(request, "stores/application_success.html")


@login_required
def dashboard(request):
    stores = Store.objects.filter(owner=request.user).prefetch_related("products")
    store = stores.filter(status=Store.Status.APPROVED).first() or stores.first()
    if not store:
        return redirect("stores:apply")
    products = store.products.select_related("category").all()
    store_orders = (
        StoreOrder.objects.filter(store=store)
        .select_related("order")
        .prefetch_related("items")
        .order_by("-created_at")
    )
    vendor_orders = []
    for store_order in store_orders:
        store_order.status_form = StoreOrderStatusForm(initial={"status": store_order.status})
        store_order.customer_label = _anonymize_customer(store_order.order.customer_name)
        store_order.phone_label = _anonymize_phone(store_order.order.customer_phone)
        vendor_orders.append(store_order)
    context = {
        "store": store,
        "stores": stores,
        "products": products,
        "active_products": products.filter(status=Product.Status.ACTIVE).count(),
        "low_stock_products": products.filter(stock__lte=5).count(),
        "vendor_orders": vendor_orders,
    }
    return render(request, "stores/dashboard.html", context)


def _anonymize_customer(value):
    words = (value or "Cliente").split()
    return " ".join((word[:1] + "***") for word in words[:2])


def _anonymize_phone(value):
    digits = "".join(character for character in (value or "") if character.isdigit())
    return "***" + digits[-2:] if digits else "Não indicado"


@login_required
@require_POST
def store_order_status(request, pk):
    store = _vendor_store(request.user)
    if not store:
        messages.error(request, "A sua loja precisa de estar aprovada para gerir pedidos.")
        return redirect("stores:dashboard")
    store_order = get_object_or_404(StoreOrder.objects.select_related("order"), pk=pk, store=store)
    form = StoreOrderStatusForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Estado de pedido inválido.")
        return redirect("stores:dashboard")

    requested_status = form.cleaned_data["status"]
    allowed_transitions = {
        Order.Status.PENDING: {Order.Status.AWAITING_PAYMENT, Order.Status.CANCELLED},
        Order.Status.AWAITING_PAYMENT: {Order.Status.PAID, Order.Status.PROCESSING, Order.Status.CANCELLED},
        Order.Status.PAID: {Order.Status.PROCESSING, Order.Status.CANCELLED},
        Order.Status.PROCESSING: {Order.Status.SHIPPED, Order.Status.CANCELLED},
        Order.Status.SHIPPED: {Order.Status.COMPLETED},
        Order.Status.COMPLETED: set(),
        Order.Status.CANCELLED: set(),
    }
    if requested_status == store_order.status:
        return redirect("stores:dashboard")
    if requested_status not in allowed_transitions.get(store_order.status, set()):
        messages.error(request, "Esta transição de estado não é permitida.")
        return redirect("stores:dashboard")

    store_order.status = requested_status
    store_order.save(update_fields=["status", "updated_at"])
    messages.success(request, "Estado do pedido atualizado com sucesso.")
    return redirect("stores:dashboard")


@login_required
def product_create(request):
    store = _vendor_store(request.user)
    if not store:
        messages.error(request, "A sua loja precisa de estar aprovada para cadastrar produtos.")
        return redirect("stores:dashboard")
    form = ProductForm(request.POST or None, request.FILES or None, store=store)
    if request.method == "POST" and form.is_valid():
        product = form.save(commit=False)
        product.store = store
        if not product.slug:
            product.slug = slugify(product.name)
        if product.status == Product.Status.ACTIVE and product.stock == 0:
            product.status = Product.Status.OUT_OF_STOCK
        product.save()
        messages.success(request, "Produto criado com sucesso.")
        return redirect("stores:dashboard")
    return render(request, "stores/product_form.html", {"form": form, "store": store, "page_title": "Novo produto", "submit_label": "Criar produto"})


@login_required
def product_edit(request, pk):
    store = _vendor_store(request.user)
    if not store:
        messages.error(request, "A sua loja precisa de estar aprovada para gerir produtos.")
        return redirect("stores:dashboard")
    product = get_object_or_404(Product, pk=pk, store=store)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product, store=store)
    if request.method == "POST" and form.is_valid():
        product = form.save(commit=False)
        if product.status == Product.Status.ACTIVE and product.stock == 0:
            product.status = Product.Status.OUT_OF_STOCK
        product.save()
        messages.success(request, "Produto atualizado com sucesso.")
        return redirect("stores:dashboard")
    return render(request, "stores/product_form.html", {"form": form, "store": store, "product": product, "page_title": "Editar produto", "submit_label": "Guardar alterações"})


@login_required
def product_delete(request, pk):
    store = _vendor_store(request.user)
    if not store:
        messages.error(request, "A sua loja precisa de estar aprovada para gerir produtos.")
        return redirect("stores:dashboard")
    product = get_object_or_404(Product, pk=pk, store=store)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Produto removido com sucesso.")
        return redirect("stores:dashboard")
    return render(request, "stores/product_confirm_delete.html", {"store": store, "product": product})


@login_required
@require_POST
def product_stock(request, pk):
    store = _vendor_store(request.user)
    if not store:
        messages.error(request, "A sua loja precisa de estar aprovada para atualizar o stock.")
        return redirect("stores:dashboard")
    product = get_object_or_404(Product, pk=pk, store=store)
    try:
        stock = int(request.POST.get("stock", ""))
    except (TypeError, ValueError):
        messages.error(request, "Indique uma quantidade de stock válida.")
        return redirect("stores:dashboard")
    if stock < 0:
        messages.error(request, "O stock não pode ser negativo.")
        return redirect("stores:dashboard")
    with transaction.atomic():
        product.stock = stock
        if stock == 0 and product.status == Product.Status.ACTIVE:
            product.status = Product.Status.OUT_OF_STOCK
        elif stock > 0 and product.status == Product.Status.OUT_OF_STOCK:
            product.status = Product.Status.DRAFT
        product.save(update_fields=["stock", "status", "updated_at"])
    messages.success(request, "Stock atualizado com sucesso.")
    return redirect("stores:dashboard")


def store_detail(request, slug):
    store = get_object_or_404(Store, slug=slug, status=Store.Status.APPROVED)
    products = Product.objects.filter(store=store, status=Product.Status.ACTIVE).select_related("category")
    return render(request, "stores/detail.html", {"store": store, "products": products})
