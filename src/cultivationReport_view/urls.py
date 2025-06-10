from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("cultivationReport_list", login_required(views.cultivationReport_list), name="cultivationReport_list"),
    path(
        "cultivationReport_list/<int:report_id>/",
        login_required(views.cultivationReport_details),
        name="cultivationReport_details",
    ),
    path(
        "edit_report/<int:report_id>/",
        login_required(views.edit_report),
        name="cultivationReport_edit",
    ),
]
