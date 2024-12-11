from django.urls import path
from . import views

# urlpatterns = [
#     path('report/', views.index, name='index'),
# ]

urlpatterns = [
    path('report/', views.daily_report_form, name='daily_report_form'),
]
