from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("productionReport_list", login_required(views.productionReport_list), name="productionReport_list"),
    path(
        "productionReport_list/<int:report_id>/",
        login_required(views.productionReport_details),
        name="productionReport_details",
    ),
    path(
        "edit_report/<int:report_id>/",
        login_required(views.edit_report),
        name="productionReport_edit",
    ),
]
