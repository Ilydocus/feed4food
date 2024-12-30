from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.dash_page, name='dashboard'),
]