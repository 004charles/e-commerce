from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, Prefetch, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from marketplace_config.api import (
    api_login_required,
    error,
    form_error,
    ok,
    serialize_order,
    serialize_user,
)
from orders.models import Order, StoreOrder

from .forms import MarketplaceUserCreationForm, ProfileForm
from .models import User


@require_http_methods(["GET", "POST"])
def login_view(request):
    """GET /account/login/ — formulário de login.
    POST /account/login/ — inicia sessão com email/username e palavra-passe."""
    accept_header = request.headers.get("Accept", "")
    is_json = (
        request.GET.get("format") == "json"
        or (request.headers.get("x-requested-with") == "XMLHttpRequest" and "text/html" not in accept_header)
        or ("application/json" in accept_header and "text/html" not in accept_header)
    )

    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("homepage:home")
        if not is_json:
            return render(request, "accounts/login.html")
        return ok({"authenticated": False})

    username_or_email = request.POST.get("username", request.POST.get("email", "")).strip()
    password = request.POST.get("password", "")
    user = None

    if username_or_email:
        # Tenta autenticar diretamente por username
        user = authenticate(request, username=username_or_email, password=password)
        if user is None:
            # Tenta autenticar por email
            user_obj = User.objects.filter(email__iexact=username_or_email).first()
            if user_obj:
                user = authenticate(request, username=user_obj.username, password=password)

    if user is None:
        if not is_json:
            return render(
                request,
                "accounts/login.html",
                {"error_message": "Nome de utilizador/e-mail ou palavra-passe incorretos."},
            )
        return error("Email ou palavra-passe inválidos.", status=401)

    login(request, user)
    if not is_json:
        next_url = request.GET.get("next") or "/"
        return redirect(next_url)
    return ok({"message": "Sessão iniciada.", "user": serialize_user(user)})


@require_http_methods(["GET", "POST"])
def logout_view(request):
    """GET/POST /account/logout/ — termina a sessão."""
    logout(request)
    accept_header = request.headers.get("Accept", "")
    is_json = (
        request.GET.get("format") == "json"
        or (request.headers.get("x-requested-with") == "XMLHttpRequest" and "text/html" not in accept_header)
        or ("application/json" in accept_header and "text/html" not in accept_header)
    )
    if not is_json:
        return redirect("homepage:home")
    return ok({"message": "Sessão terminada."})


@require_http_methods(["GET", "POST"])
def register(request):
    """GET /account/register/ — formulário de registo.
    POST /account/register/ — cria conta e inicia sessão."""
    accept_header = request.headers.get("Accept", "")
    is_json = (
        request.GET.get("format") == "json"
        or (request.headers.get("x-requested-with") == "XMLHttpRequest" and "text/html" not in accept_header)
        or ("application/json" in accept_header and "text/html" not in accept_header)
    )

    if request.user.is_authenticated:
        if not is_json:
            return redirect("homepage:home")
        return error("Já tem sessão iniciada.", status=409)

    if request.method == "GET":
        if not is_json:
            return render(request, "accounts/register.html")
        return ok({"message": "Registo de conta"})

    email = request.POST.get("email", "").strip().lower()
    username = request.POST.get("username", email).strip()
    password = request.POST.get("password", "")
    password_confirm = request.POST.get("password_confirm", password)

    if password != password_confirm:
        if not is_json:
            return render(
                request,
                "accounts/register.html",
                {"error_message": "As palavras-passe introduzidas não coincidem."},
            )
        return error("As palavras-passe não coincidem.", status=400)

    form = MarketplaceUserCreationForm(
        {
            "username": username,
            "email": email,
            "phone": request.POST.get("phone", "").strip(),
            "password1": password,
            "password2": password_confirm,
        }
    )
    if not form.is_valid():
        if not is_json:
            first_err = next(iter(form.errors.values()))[0] if form.errors else "Erro de validação."
            return render(request, "accounts/register.html", {"error_message": first_err})
        return form_error(form)

    user = form.save(commit=False)
    user.first_name = request.POST.get("first_name", "").strip()
    user.last_name = request.POST.get("last_name", "").strip()
    user.save()
    login(request, user)

    if not is_json:
        return redirect("homepage:home")
    return ok({"message": "Conta criada com sucesso.", "user": serialize_user(user)}, status=201)


@require_GET
def session_status(request):
    """GET /account/session-status/ — quem está autenticado."""
    if not request.user.is_authenticated:
        return ok({"authenticated": False, "user": None})
    return ok({"authenticated": True, "user": serialize_user(request.user)})


@require_POST
def password_reset(request):
    """POST /account/password-reset/ — envia email de recuperação."""
    from django.contrib.auth.forms import PasswordResetForm

    form = PasswordResetForm({"email": request.POST.get("email", "").strip().lower()})
    if not form.is_valid():
        return form_error(form, "Introduza um email válido.")
    form.save(request=request, use_https=request.is_secure())
    return ok(
        {
            "message": "Se o email existir, receberá instruções para redefinir a palavra-passe."
        }
    )


@require_http_methods(["GET", "POST"])
def profile(request):
    """GET  /account/profile/ — perfil e resumo da conta.
    POST /account/profile/ — atualiza os dados pessoais."""
    if not request.user.is_authenticated:
        return redirect("/account/login/?next=/account/profile/")

    accept_header = request.headers.get("Accept", "")
    is_json = (
        request.GET.get("format") == "json"
        or (request.headers.get("x-requested-with") == "XMLHttpRequest" and "text/html" not in accept_header)
        or ("application/json" in accept_header and "text/html" not in accept_header)
    )

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if not form.is_valid():
            if not is_json:
                return render(request, "accounts/profile.html", {"user": request.user, "errors": form.errors})
            return form_error(form)
        form.save()
        if not is_json:
            return redirect("accounts:profile")
        return ok({"message": "O seu perfil foi atualizado.", "user": serialize_user(request.user)})

    if not is_json:
        return render(request, "accounts/profile.html", {"user": request.user})

    user_orders = Order.objects.filter(user=request.user)
    spent = (
        user_orders.filter(payment_status=Order.PaymentStatus.PAID)
        .aggregate(total=Sum("total"))
        .get("total")
        or 0
    )
    return ok(
        {
            "user": serialize_user(request.user),
            "summary": {
                "order_count": user_orders.count(),
                "open_order_count": user_orders.exclude(
                    status__in=[Order.Status.COMPLETED, Order.Status.CANCELLED]
                ).count(),
                "total_spent": str(spent),
                "currency": "AOA",
            },
            "recent_orders": [
                serialize_order(request, order) for order in user_orders[:10]
            ],
        }
    )


@api_login_required
@require_GET
def order_list(request):
    """GET /account/orders/ — pedidos do utilizador autenticado."""
    orders = Order.objects.filter(user=request.user).annotate(
        store_count=Count("store_orders")
    )
    return ok(
        {
            "count": orders.count(),
            "results": [
                dict(serialize_order(request, order), store_count=order.store_count)
                for order in orders
            ],
        }
    )


@api_login_required
@require_GET
def order_detail(request, order_number):
    """GET /account/orders/<numero>/ — detalhe de um pedido."""
    order = get_object_or_404(
        Order.objects.filter(user=request.user).prefetch_related(
            Prefetch(
                "store_orders",
                queryset=StoreOrder.objects.select_related("store").prefetch_related("items"),
            )
        ),
        order_number=order_number,
    )
    return ok({"order": serialize_order(request, order, detail=True)})
