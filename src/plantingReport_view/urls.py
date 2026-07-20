from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("plantingReport_list", login_required(views.plantingReport_list), name="plantingReport_list"),
    path(
        "plantingReport_list/<int:report_id>/",
        login_required(views.plantingReport_details),
        name="plantingReport_details",
    ),
    path(
        "edit_report/<int:report_id>/",
        login_required(views.edit_report),
        name="plantingReport_edit",
    ),
]
