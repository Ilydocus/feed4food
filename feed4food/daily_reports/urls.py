from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import ProduceReportView

urlpatterns = [
    path('report_form', login_required(ProduceReportView.as_view()), name='report_form')
]
