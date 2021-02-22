from django.urls import path
from . import views

urlpatterns = [
    path("", views.AllPlayers.as_view()),
    path("search", views.AllPlayers.as_view()),
    path("<slug:slug>/", views.ProfilePlayer.as_view()),
]
