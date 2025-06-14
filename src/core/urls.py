"""
URL configuration for website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("productionReport/", include("productionReport.urls")),
    path("productionReport_list/", include("productionReport_view.urls")),
    path("", include("django_prometheus.urls")),
    path("django_plotly_dash/", include("django_plotly_dash.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("personalDashboard/", include("personalDashboard.urls")),
    path("grafanaDashboard/", include("personalDashboard.urls")),
    path("data_portal/", TemplateView.as_view(template_name="data_portal.html"), name="data_portal"),
    path("add_data_portal/", TemplateView.as_view(template_name="add_data_portal.html"), name="add_data_portal"),
    path("view_data_portal/", TemplateView.as_view(template_name="view_data_portal.html"), name="view_data_portal"),
    path('feedback/', include('feedback.urls')),
    path("financialReport/", include("financialReport.urls")),
    path("financialReport_list/", include("financialReport_view.urls")),
    path("wasteReport/", include("wasteReport.urls")),
    path("wasteReport_list/", include("wasteReport_view.urls")),
    path("waterReport/", include("waterReport.urls")),
    path("waterReport_list/", include("waterReport_view.urls")),
    path("salesReport/", include("salesReport.urls")),
    path("salesReport_list/", include("salesReport_view.urls")),
    path("eventReport/", include("eventReport.urls")),
    path("eventReport_list/", include("eventReport_view.urls")),
    path("demographicReport/", include("demographicReport.urls")),
    path("demographicReport_list/", include("demographicReport_view.urls")),
    path("cultivationReport/", include("cultivationReport.urls")),
    path("cultivationReport_list/", include("cultivationReport_view.urls")),
    path("inputReport/", include("inputReport.urls")),
    path("inputReport_list/", include("inputReport_view.urls")),
    path("lluseReport/", include("lluseReport.urls")),
    path("lluseReport_list/", include("lluseReport_view.urls")),
]
