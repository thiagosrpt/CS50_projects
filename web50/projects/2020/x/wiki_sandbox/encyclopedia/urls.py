from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.index, name="wiki_index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("new/", views.new_entry, name="new_entry"),
    path("random/", views.random_page, name="random_page"),
    path("edit/<str:title>", views.edit, name="edit")
]
