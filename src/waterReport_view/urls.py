from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("waterReport_list", login_required(views.waterReport_list), name="waterReport_list"),
    path(
        "waterReport_list/<int:report_id>/",
        login_required(views.waterReport_details),
        name="waterReport_details",
    ),
    path(
        "edit_report/<int:report_id>/",
        login_required(views.edit_report),
        name="waterReport_edit",
    ),
]
