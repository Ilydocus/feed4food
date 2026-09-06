from django.db import models
from django.contrib.auth.models import User
from core.reportUtils import PartnerCities


class StagedRow(models.Model):
    STATUS_CHOICES = [
        ("auto_approved", "Auto Approved"),     # clean match, ready to commit
        ("needs_review", "Needs Review"),       # blocks commit until resolved
        ("approved", "Approved"),               # user edited + it now resolves
        ("rejected", "Rejected"),               # user gave up on this row
        ("duplicate", "Duplicate"),             # already in DB, informational
        ("not_supported", "Not Supported"),     # e.g. Planting - no table yet
        ("ignored", "Ignored"),                 # e.g. Pruning - not in scope
        ("unknown", "Unknown Action Type"),
        ("committed", "Committed"),             # written to real tables
    ]

    # Statuses that must all be cleared before a batch can be committed
    BLOCKING_STATUSES = ["needs_review"]
    # Statuses that get written to the real tables on commit
    INSERTABLE_STATUSES = ["auto_approved", "approved"]

    upload_batch = models.CharField(max_length=100)
    source_row_number = models.IntegerField(null=True, blank=True)
    action_type = models.CharField(max_length=50)
    living_lab = models.CharField(max_length=100, choices=PartnerCities.choices, default=PartnerCities.Drama)

    raw_data = models.JSONField()
    corrected_data = models.JSONField()
    message = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="needs_review")
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    # Staged rows are kept indefinitely - even after commit/reject - as an
    # audit trail. There is currently no cleanup/expiry job.

    def __str__(self):
        return f"{self.action_type} row {self.source_row_number} ({self.status})"