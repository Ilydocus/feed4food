from django.urls import path
from .views import register, pending_activation


urlpatterns = [
    path("register/", register, name="register"),
    path("pending_activation/", pending_activation, name="pending_activation"),
]
