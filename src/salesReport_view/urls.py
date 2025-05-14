from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("salesReport_list", login_required(views.salesReport_list), name="salesReport_list"),
    path(
        "salesReport_list/<int:report_id>/",
        login_required(views.salesReport_details),
        name="salesReport_details",
    ),
    path(
        "edit_report/<int:report_id>/",
        login_required(views.edit_report),
        name="salesReport_edit",
    ),
]
