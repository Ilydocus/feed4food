from .views import get_post_report, get_groups_by_city
from django.urls import path
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("demographicReport", login_required(get_post_report), name="demographicReport"),
    path('get-groups-by-city/', get_groups_by_city, name='get_groups_by_city'),
]