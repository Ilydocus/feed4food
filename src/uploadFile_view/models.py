from django.db import models
from django.contrib.auth.models import User

class StagedRow(models.Model):
    STATUS_CHOICES = [
        ("auto_approved", "Auto Approved"),
        ("needs_review", "Needs Review"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    upload_batch = models.CharField(max_length=100)
    source_row_number = models.IntegerField(null=True, blank=True)
    action_type = models.CharField(max_length=50)

    raw_data = models.JSONField()
    corrected_data = models.JSONField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="needs_review")
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.action_type} row {self.source_row_number} ({self.status})"