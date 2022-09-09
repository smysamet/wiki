from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("search/", views.search, name="search"),
    path("random-page/", views.randomPage, name="random-page"),
    path("new-page/", views.newPage, name="new-page"),
    path("edit-entry/<str:title>", views.editEntry, name="edit-entry")
]
