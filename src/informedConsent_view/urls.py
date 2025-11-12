from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.informedConsent_show), name='informedConsent_show'),
    path('download/', login_required(views.download_informedConsent), name='download_informedConsent'),
]