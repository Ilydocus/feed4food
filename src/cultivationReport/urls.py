from .views import get_post_report
from productionReport.views import get_locations, get_gardens
from django.urls import path
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("cultivationReport", login_required(get_post_report), name="cultivationReport"),
    path('ajax/get-locations/', get_locations, name='ajax_get_locations'), 
    path('ajax/get-gardens/', get_gardens, name='ajax_get_gardens'), 
]