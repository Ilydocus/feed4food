from .views import get_post_report, get_inputs_by_city
from productionReport.views import get_locations, get_gardens
from django.urls import path
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("inputReport", login_required(get_post_report), name="inputReport"),
    path('ajax/get-locations/', get_locations, name='ajax_get_locations'), 
    path('ajax/get-gardens/', get_gardens, name='ajax_get_gardens'),
    path('get-inputs-by-city/', get_inputs_by_city, name='get_inputs_by_city'),  
]