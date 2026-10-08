from django.urls import path

from . import views


app_name = "homepage"

urlpatterns = [
    path("", views.home, name="home"),
    path("materiais-construcao/", views.materiais_construcao, name="materiais-construcao"),
    path("mobilias/", views.mobilias, name="mobilias"),
    path("criancas/", views.criancas, name="criancas"),
    path("plantas-vasos/", views.plantas_vasos, name="plantas-vasos"),
    path("sobre-nos/", views.about, name="about"),
    path("about/", views.about, name="about-alt"),
    path("contacto/", views.contact, name="contact"),
    path("contact/", views.contact, name="contact-alt"),
    path("carreiras/", views.careers, name="careers"),
    path("careers/", views.careers, name="careers-alt"),
    path("termos/", views.terms, name="terms"),
    path("terms/", views.terms, name="terms-alt"),
    path("home/data/", views.home_data, name="home-data"),
    path("home/site-data/", views.site_data, name="site-data"),
    path("home/search/", views.search_data, name="search-data"),
]
