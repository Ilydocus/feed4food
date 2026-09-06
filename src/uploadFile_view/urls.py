from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("uploadFile_list/<str:batch_id>/", login_required(views.uploadFile_list_batch), name="uploadFile_list_batch"),
    path("uploadFile_row/<int:row_id>/", login_required(views.uploadFile_details), name="uploadFile_details"),
    path("uploadFile_row/<int:row_id>/edit/", login_required(views.edit_row), name="uploadFile_edit"),
    path("uploadFile_row/<int:row_id>/suggestion/", login_required(views.apply_suggestion), name="uploadFile_suggestion"),
    path("uploadFile_row/<int:row_id>/split/", login_required(views.confirm_split), name="uploadFile_confirm_split"),
    path("uploadFile_row/<int:row_id>/reject/", login_required(views.reject_row), name="uploadFile_reject"),
    path("uploadFile_commit/<str:batch_id>/", login_required(views.commit_batch), name="uploadFile_commit"),
]