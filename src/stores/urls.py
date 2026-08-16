from django.urls import path

from . import views


app_name = "stores"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/products/new/", views.product_create, name="product-create"),
    path("dashboard/products/<int:pk>/edit/", views.product_edit, name="product-edit"),
    path("dashboard/products/<int:pk>/delete/", views.product_delete, name="product-delete"),
    path("dashboard/products/<int:pk>/stock/", views.product_stock, name="product-stock"),
    path("dashboard/orders/<int:pk>/status/", views.store_order_status, name="order-status"),
    path("apply/", views.apply, name="apply"),
    path("apply/success/", views.application_success, name="application-success"),
    path("<slug:slug>/", views.store_detail, name="detail"),
]
