from django.db import models
from django.contrib.auth.models import User
from core import reportUtils
from demographicReport.models import UnderrepresentedGroup


class LLUseReport(models.Model):
        
    report_id = models.AutoField(blank=False, null=False, unique=True, primary_key=True)

    report_date = models.DateField()

    creation_time = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    city = models.CharField(max_length=100, choices=reportUtils.PartnerCities)

    gardens_in_use = models.IntegerField(default=0)
    total_ll_participants = models.IntegerField(default=0)

class LLUseReportPerUnderrepresentedGroups(models.Model):
    name = models.ForeignKey(UnderrepresentedGroup, on_delete=models.SET_NULL, null=True)
    report_id = models.ForeignKey(
        LLUseReport, on_delete=models.CASCADE, related_name="perunderrepresentedgroups"
    )
    ll_participants = models.IntegerField()

