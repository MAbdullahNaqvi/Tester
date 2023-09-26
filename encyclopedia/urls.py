from django.urls import path

from . import views

urlpatterns = [
    path("wiki/<str:entry>/", views.entry, name ="entry"),
    path("", views.index, name="index"),
    path("search", views.search, name = "search"),
    path("AddEntry", views.add_entry, name = "AddEntry" ),
    path("EditEntry", views.edit_entry, name = "EditEntry"),
    path("Random", views.random, name = "random")
]
