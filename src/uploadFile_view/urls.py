from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("uploadFile_list", login_required(views.uploadFile_list), name="uploadFile_list"),
    path("uploadFile_list/<int:upload_id>/", login_required(views.uploadFile_details), name="uploadFile_details"),
]