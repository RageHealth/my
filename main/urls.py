from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),
    path("o nas", views.about, name="about"),
    path("kontakti", views.contacts, name="contacts"),
    path("novosti", views.news, name="news"),
]