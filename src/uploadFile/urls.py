from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import upload_file_view, locations_for_living_lab, gardens_for_location

urlpatterns = [
    path("upload_file", login_required(upload_file_view), name="upload_file"),
    path("ajax/locations/", locations_for_living_lab, name="ajax_locations"),
    path("ajax/gardens/", gardens_for_location, name="ajax_gardens"),
]