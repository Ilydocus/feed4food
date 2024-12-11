from django.urls import path
from . import views

# urlpatterns = [
#     path('report/', views.index, name='index'),
# ]

urlpatterns = [
    path('report/', views.daily_report_form, name='daily_report_form'),
]

from django.urls import path
from .views import report_form, item_details

urlpatterns = [
    path('report-form/', report_form, name='report_form'),
    path('item-details/<int:item_id>/', item_details, name='item_details'),
]
