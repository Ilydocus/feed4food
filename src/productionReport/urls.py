from .views import get_post_report, get_locations
from django.urls import path
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("report_form", login_required(get_post_report), name="report_form"),
    #path('get-locations/', get_locations, name='get_locations'),
    path('ajax/get-locations/', get_locations, name='ajax_get_locations'), 
]
