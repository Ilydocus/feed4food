from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import get_post_report, get_item_attributes, get_map_test

urlpatterns = [
    path('report_form', login_required(get_post_report), name='report_form'),
    path('get_item/<str:name>', login_required(get_item_attributes), name='get_item_attributes'),
    path('map_test', login_required(get_map_test), name='map_test'),
]
