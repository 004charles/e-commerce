from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [
    path("order/<str:order_number>/select/", views.select_payment, name="select"),
    path("order/<str:order_number>/pending/", views.pending, name="pending"),
]
