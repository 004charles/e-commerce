from django.urls import path

from . import views


app_name = "catalog"

urlpatterns = [
    path("", views.product_list, name="list"),
    path("categories/", views.category_list, name="category-list"),
    path("category/<slug:category_slug>/", views.product_list, name="category"),
    path(
        "product/<slug:store_slug>/<slug:slug>/index.html",
        views.legacy_product_detail,
        name="legacy-detail",
    ),
    path(
        "product/<slug:store_slug>/<slug:slug>/",
        views.product_detail,
        name="detail",
    ),
    path(
        "product/<slug:store_slug>/<slug:slug>/review/",
        views.submit_review,
        name="submit-review",
    ),
]
