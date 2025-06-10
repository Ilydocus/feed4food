from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("demographicReport_list", login_required(views.demographicReport_list), name="demographicReport_list"),
    path(
        "demographicReport_list/<int:report_id>/",
        login_required(views.demographicReport_details),
        name="demographicReport_details",
    ),
    path(
        "edit_report/<int:report_id>/",
        login_required(views.edit_report),
        name="demographicReport_edit",
    ),
]
