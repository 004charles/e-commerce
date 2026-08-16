from django.urls import path

from . import views


app_name = "cart"

urlpatterns = [
    path("api/", views.summary, name="summary"),
    path("api/add/", views.add_item, name="add"),
    path("api/update/", views.update_item, name="update"),
    path("api/remove/", views.remove_item, name="remove"),
]
