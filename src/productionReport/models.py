from django.db import models
from django.contrib.auth.models import User
from core import reportUtils


class Product(models.Model):
    name = models.CharField(
        max_length=100, blank=False, null=False, unique=True, primary_key=True
    )
    latin_name = models.CharField(max_length=100, blank=True, null=True)
    living_lab = models.CharField(choices=reportUtils.PartnerCities, max_length=100, blank=False)
    native_variety = models.BooleanField()
    unit = models.CharField(max_length=100, blank=False, null=False)

class LLLocation(models.Model):
    name = models.CharField(
        max_length=100, blank=False, null=False, unique=True, primary_key=True
    )
    living_lab = models.CharField(choices=reportUtils.PartnerCities, max_length=100, blank=False)

class Garden(models.Model):
    name = models.CharField(
        max_length=100, blank=False, null=False, unique=True, primary_key=True
    )
    living_lab = models.CharField(choices=reportUtils.PartnerCities, max_length=100, blank=False)


class ProductionReport(models.Model):
    report_id = models.AutoField(blank=False, null=False, unique=True, primary_key=True)

    creation_time = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    city = models.CharField(max_length=100, choices=reportUtils.PartnerCities)
    location = models.ForeignKey(LLLocation, on_delete=models.SET_NULL, null=True)
    garden = models.CharField(max_length=100)


class ProductionReportDetails(models.Model):
    name = models.ForeignKey(Product, on_delete=models.CASCADE)
    report_id = models.ForeignKey(
        ProductionReport, on_delete=models.CASCADE, related_name="details"
    )
    production_date = models.DateField(null=True)
    quantity = models.FloatField()

