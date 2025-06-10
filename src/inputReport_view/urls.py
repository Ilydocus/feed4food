from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("inputReport_list", login_required(views.inputReport_list), name="inputReport_list"),
    path(
        "inputReport_list/<int:report_id>/",
        login_required(views.inputReport_details),
        name="inputReport_details",
    ),
    path(
        "edit_report/<int:report_id>/",
        login_required(views.edit_report),
        name="inputReport_edit",
    ),
]
