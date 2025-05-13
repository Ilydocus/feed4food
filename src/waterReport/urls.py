from .views import get_post_report
from django.urls import path
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("waterReport", login_required(get_post_report), name="waterReport"),
]
