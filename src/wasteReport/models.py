from django.db import models
from django.contrib.auth.models import User
from core import reportUtils
from productionReport.models import LLLocation, Garden

class WasteType(models.Model):
    name = models.CharField(
        max_length=100, blank=False, null=False, unique=True, primary_key=True
    )
    is_organic =models.BooleanField(default=False)
    unit = models.CharField(max_length=100, blank=False, null=False)
    living_lab = models.CharField(max_length=100, choices=reportUtils.PartnerCities)

class WasteReport(models.Model):
    report_id = models.AutoField(blank=False, null=False, unique=True, primary_key=True)

    creation_time = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    city = models.CharField(max_length=100, choices=reportUtils.PartnerCities)
    location = models.ForeignKey(LLLocation, on_delete=models.SET_NULL, null=True)
    garden = models.ForeignKey(Garden, on_delete=models.SET_NULL, null=True)



class WasteReportDetails(models.Model):
    date = models.DateField()
    wasteType = models.ForeignKey(WasteType, on_delete=models.CASCADE)
    wasteAction = models.CharField(max_length=100, choices=reportUtils.WasteActions)
    report_id = models.ForeignKey(
        WasteReport, on_delete=models.CASCADE, related_name="details"
    )
    quantity = models.FloatField()



