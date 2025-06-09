from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("wasteReport_list", login_required(views.wasteReport_list), name="wasteReport_list"),
    path(
        "wasteReport_list/<int:report_id>/",
        login_required(views.wasteReport_details),
        name="wasteReport_details",
    ),
    path(
        "edit_report/<int:report_id>/",
        login_required(views.edit_report),
        name="wasteReport_edit",
    ),
]
