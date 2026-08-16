from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


app_name = "accounts"

urlpatterns = [
    path("login/", views.MarketplaceLoginView.as_view(), name="login"),
    path("logout/", views.MarketplaceLogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("session-status/", views.session_status, name="session-status"),
    path("profile/", views.profile, name="profile"),
    path("orders/", views.order_list, name="order-list"),
    path("orders/<str:order_number>/", views.order_detail, name="order-detail"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
        name="password_reset",
    ),
    path("modal/login/", views.modal_login, name="modal_login"),
    path("modal/register/", views.modal_register, name="modal_register"),
    path("modal/password-reset/", views.modal_password_reset, name="modal_password_reset"),
]
