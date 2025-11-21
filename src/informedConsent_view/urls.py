from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView

urlpatterns = [
    #path('', login_required(views.informedConsent_show), name='informedConsent_view'),
    path("", login_required(TemplateView.as_view(template_name="informedConsent_show.html")), name="informedConsent_view"),
    path('download/', login_required(views.download_informedConsent), name='download_informedConsent'),
]