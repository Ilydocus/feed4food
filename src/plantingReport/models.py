from django.db import models
from django.contrib.auth.models import User
from core import reportUtils
from productionReport.models import Product, LLLocation, Garden


class PlantingReport(models.Model):
    report_id = models.AutoField(blank=False, null=False, unique=True, primary_key=True)

    creation_time = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    city = models.CharField(max_length=100, choices=reportUtils.PartnerCities)
    location = models.ForeignKey(LLLocation, on_delete=models.SET_NULL, null=True)
    garden = models.ForeignKey(Garden, on_delete=models.SET_NULL, null=True)

    planting_date = models.DateField(null=True)


class PlantingReportDetails(models.Model):
    name = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    report_id = models.ForeignKey(
        PlantingReport, on_delete=models.CASCADE, related_name="details"
    )
    area_quantity_planted = models.FloatField()
    planting_unit = models.CharField(choices=reportUtils.CultivationTypes, max_length=100, blank=False, default=reportUtils.CultivationTypes.Surface)


