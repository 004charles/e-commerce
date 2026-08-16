from django.urls import path

from . import views


app_name = "homepage"

urlpatterns = [
    path("", views.home, name="home"),
    path("home/data/", views.home_data, name="home-data"),
    path("home/search/", views.search_data, name="search-data"),
]
