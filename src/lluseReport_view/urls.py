from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("lluseReport_list", login_required(views.lluseReport_list), name="lluseReport_list"),
    path(
        "lluseReport_list/<int:report_id>/",
        login_required(views.lluseReport_details),
        name="lluseReport_details",
    ),
    path(
        "edit_report/<int:report_id>/",
        login_required(views.edit_report),
        name="lluseReport_edit",
    ),
]
