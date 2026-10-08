from django.urls import path

from . import views


app_name = "accounts"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("session-status/", views.session_status, name="session-status"),
    path("password-reset/", views.password_reset, name="password-reset"),
    path("profile/", views.profile, name="profile"),
    path("orders/", views.order_list, name="order-list"),
    path("orders/<str:order_number>/", views.order_detail, name="order-detail"),
]
