from django.contrib import messages
from django.db.models import Count, Prefetch
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from urllib.parse import quote

from .forms import MarketplaceAuthenticationForm, MarketplaceUserCreationForm, ProfileForm
from orders.models import Order, StoreOrder

from .models import User


class MarketplaceLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = MarketplaceAuthenticationForm
    redirect_authenticated_user = True

    def get(self, request, *args, **kwargs):
        next_url = request.GET.get("next", "/")
        return redirect(f"/?open_auth=1&next={quote(next_url, safe='')}")


class MarketplaceLogoutView(LogoutView):
    next_page = "/"
    http_method_names = ["get", "post", "options"]

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(self.next_page)


def register(request):
    if request.user.is_authenticated:
        return redirect("accounts:profile")
    form = MarketplaceUserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "A sua conta foi criada com sucesso.")
        return redirect("accounts:profile")
    return render(request, "accounts/register.html", {"form": form})


def session_status(request):
    if not request.user.is_authenticated:
        return JsonResponse({"authenticated": False})
    return JsonResponse(
        {
            "authenticated": True,
            "name": request.user.get_full_name() or request.user.email or request.user.username,
            "profile_url": "/account/profile/",
            "orders_url": "/account/orders/",
            "logout_url": "/account/logout/",
        }
    )


@require_POST
def modal_login(request):
    email = request.POST.get("email", "").strip().lower()
    password = request.POST.get("password", "")
    user = None
    if email:
        try:
            username = User.objects.get(email__iexact=email).username
        except User.DoesNotExist:
            username = None
        if username:
            user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({"ok": False, "message": "Email ou palavra-passe inválidos."}, status=400)
    login(request, user)
    return JsonResponse({"ok": True, "message": "Sessão iniciada.", "redirect": "/account/profile/"})


@require_POST
def modal_register(request):
    form = MarketplaceUserCreationForm(
        {
            "username": request.POST.get("email", "").strip().lower(),
            "email": request.POST.get("email", "").strip().lower(),
            "phone": request.POST.get("phone", "").strip(),
            "password1": request.POST.get("password", ""),
            "password2": request.POST.get("password", ""),
        }
    )
    if not request.POST.get("terms"):
        return JsonResponse({"ok": False, "message": "É necessário aceitar os termos."}, status=400)
    if not form.is_valid():
        return JsonResponse({"ok": False, "message": "Verifique os dados introduzidos.", "errors": form.errors}, status=400)
    user = form.save(commit=False)
    full_name = request.POST.get("full_name", "").strip()
    parts = full_name.split(maxsplit=1)
    user.first_name = parts[0] if parts else ""
    user.last_name = parts[1] if len(parts) > 1 else ""
    user.save()
    login(request, user)
    return JsonResponse({"ok": True, "message": "Conta criada com sucesso.", "redirect": "/account/profile/"})


@require_POST
def modal_password_reset(request):
    from django.contrib.auth.forms import PasswordResetForm

    email = request.POST.get("email", "").strip().lower()
    form = PasswordResetForm({"email": email})
    if not form.is_valid():
        return JsonResponse({"ok": False, "message": "Introduza um email válido."}, status=400)
    form.save(request=request, use_https=request.is_secure())
    return JsonResponse({"ok": True, "message": "Se o email existir, receberá instruções para redefinir a palavra-passe."})


@login_required
def profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "O seu perfil foi atualizado.")
        return redirect("accounts:profile")
    orders = Order.objects.filter(user=request.user).annotate(store_count=Count("store_orders"))[:10]
    return render(request, "accounts/profile.html", {"form": form, "orders": orders})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).annotate(store_count=Count("store_orders"))
    return render(request, "accounts/order_list.html", {"orders": orders})


@login_required
def order_detail(request, order_number):
    order = get_object_or_404(
        Order.objects.filter(user=request.user)
        .prefetch_related(
            Prefetch(
                "store_orders",
                queryset=StoreOrder.objects.select_related("store").prefetch_related("items"),
            )
        ),
        order_number=order_number,
    )
    return render(request, "accounts/order_detail.html", {"order": order})
