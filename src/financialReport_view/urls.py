from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("financialReport_list", login_required(views.financialReport_list), name="financialReport_list"),
    path(
        "financialReport_list/<int:report_id>/",
        login_required(views.financialReport_details),
        name="financialReport_details",
    ),
    path(
        "edit_report/<int:report_id>/",
        login_required(views.edit_report),
        name="financialReport_edit",
    ),
]
