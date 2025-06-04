from .views import get_post_report, get_locations, get_gardens
from django.urls import path
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("cultivationReport", login_required(get_post_report), name="cultivationReport"),
    path('ajax/get-locations_c/', get_locations, name='ajax_get_locations_c'), 
    path('ajax/get-gardens_c/', get_gardens, name='ajax_get_gardens_c'), 
]