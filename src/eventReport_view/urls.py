from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("eventReport_list", login_required(views.eventReport_list), name="eventReport_list"),
    path(
        "eventReport_list/<int:report_id>/",
        login_required(views.eventReport_details),
        name="eventReport_details",
    ),
    path(
        "edit_report/<int:report_id>/",
        login_required(views.edit_report),
        name="eventReport_edit",
    ),
]
