from .views import get_post_report
from demographicReport.views import get_groups_by_city
from django.urls import path
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("lluseReport", login_required(get_post_report), name="lluseReport"),
    path('get-groups-by-city/', get_groups_by_city, name='get_groups_by_city'),
]