from .views import get_post_report, get_locations, get_gardens, get_products_by_city
from django.urls import path
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("productionReport_form", login_required(get_post_report), name="productionReport_form"),
    path('ajax/get-locations/', get_locations, name='ajax_get_locations'), 
    path('ajax/get-gardens/', get_gardens, name='ajax_get_gardens'),
    path('get-products-by-city/', get_products_by_city, name='get_products_by_city'), 
]
