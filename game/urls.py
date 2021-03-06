from django.contrib import admin
from django.urls import path

from .views import LoginView, CardView, AdminCardView

app_name = "game"

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("card/<uuid:pk>", CardView.as_view(), name="card"),
    path("card/<uuid:pk>/admin", AdminCardView.as_view(), name="admin"),
]
