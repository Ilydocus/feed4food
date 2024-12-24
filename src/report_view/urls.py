from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('report_list', login_required(views.report_list), name='report_list'),
    path('report_list/<int:report_id>/', login_required(views.report_details), name='report_details'),
    path('edit_report/<int:report_id>/', login_required(views.edit_report), name='report_edit'),
]
