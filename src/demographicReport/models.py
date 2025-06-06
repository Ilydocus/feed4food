from django.db import models
from django.contrib.auth.models import User
from core import reportUtils

class UnderrepresentedGroup(models.Model):
    name = models.CharField(
        max_length=100, blank=False, null=False, unique=True, primary_key=True
    )
    living_lab = models.CharField(max_length=100, choices=reportUtils.PartnerCities)

class DemographicReport(models.Model):
        
    report_id = models.AutoField(blank=False, null=False, unique=True, primary_key=True)

    data_date = models.DateField()

    creation_time = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    city = models.CharField(max_length=100, choices=reportUtils.PartnerCities)

    #Total population
    total_population = models.IntegerField(default=0)

class DemographicReportPerUnderrepresentedGroups(models.Model):
    name = models.ForeignKey(UnderrepresentedGroup, on_delete=models.SET_NULL, null=True)
    report_id = models.ForeignKey(
        DemographicReport, on_delete=models.CASCADE, related_name="perunderrepresentedgroups"
    )
    population = models.IntegerField()

