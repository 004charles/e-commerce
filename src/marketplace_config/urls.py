from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

from cart import views as cart_views


urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
    path("account/", include("accounts.urls")),
    path("", include("homepage.urls")),
    path("catalog/", include("catalog.urls")),
    path("cart.html", cart_views.legacy_cart_page, name="legacy-cart"),
    path("cart/", include("cart.urls")),
    path("stores/", include("stores.urls")),
    path("orders/", include("orders.urls")),
    path("payments/", include("payments.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        re_path(
            r"^assets/(?P<path>.*)$",
            serve,
            {"document_root": settings.BASE_DIR / "assets"},
        )
    ]
