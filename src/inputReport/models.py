from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from core import reportUtils
from productionReport.models import Product, LLLocation, Garden

class Input(models.Model):
    name = models.CharField(
        max_length=100, blank=False, null=False, unique=True, primary_key=True
    )
    detailed_reference = models.CharField(max_length=100, default="", null=True)
    input_type = models.CharField(max_length=100, choices=reportUtils.InputType)
    unit = models.CharField(max_length=20)
    input_category = models.CharField(max_length=100, choices=reportUtils.InputCategory)
    active_ingredient = models.CharField(max_length=100, default="")
    living_lab = models.CharField(max_length=100, choices=reportUtils.PartnerCities)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

class InputReport(models.Model):
        
    report_id = models.AutoField(blank=False, null=False, unique=True, primary_key=True)

    application_date = models.DateField()

    creation_time = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    city = models.CharField(max_length=100, choices=reportUtils.PartnerCities)
    location = models.ForeignKey(LLLocation, on_delete=models.SET_NULL, null=True)
    garden = models.ForeignKey(Garden, on_delete=models.SET_NULL, null=True)


class InputReportDetails(models.Model):
    name_input = models.ForeignKey(Input, on_delete=models.SET_NULL, null=True)
    name_product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    report_id = models.ForeignKey(
        InputReport, on_delete=models.CASCADE, related_name="details"
    )
    area = models.FloatField()
    quantity = models.FloatField()