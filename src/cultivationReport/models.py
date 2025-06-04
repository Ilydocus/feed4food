from django.db import models
from django.contrib.auth.models import User
from core import reportUtils
from productionReport.models import Product, LLLocation, Garden


class CultivationReport(models.Model):
    report_id = models.AutoField(blank=False, null=False, unique=True, primary_key=True)

    creation_time = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    city = models.CharField(max_length=100, choices=reportUtils.PartnerCities)
    location = models.ForeignKey(LLLocation, on_delete=models.SET_NULL, null=True)
    garden = models.ForeignKey(Garden, on_delete=models.SET_NULL, null=True)

    cultivation_date = models.DateField(null=True)


class CultivationReportDetails(models.Model):
    name = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    report_id = models.ForeignKey(
        CultivationReport, on_delete=models.CASCADE, related_name="details"
    )
    area_cultivated = models.FloatField()


