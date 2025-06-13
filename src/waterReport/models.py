from django.db import models
from django.contrib.auth.models import User
from core import reportUtils
from productionReport.models import LLLocation, Garden

class WaterReport(models.Model):
    report_id = models.AutoField(blank=False, null=False, unique=True, primary_key=True)

    creation_time = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    city = models.CharField(max_length=100, choices=reportUtils.PartnerCities)
    location = models.ForeignKey(LLLocation, on_delete=models.SET_NULL, null=True)
    garden = models.ForeignKey(Garden, on_delete=models.SET_NULL, null=True)



class WaterReportRainfall(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    report_id = models.ForeignKey(
        WaterReport, on_delete=models.CASCADE, related_name="rainfalls"
    )
    quantity = models.FloatField()

class WaterReportIrrigation(models.Model):
    class FrequencyInterval(models.TextChoices):
        DAY = 'day', 'day'
        WEEK = 'week', 'week'
        MONTH = 'month', 'month'
    class WaterSources(models.TextChoices):
        HARVESTED = 'harvested','Harvested water'
        TAP = 'tap', 'Tap water'
        OTHER = 'other', 'Other'
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    period = models.BooleanField()
    source = frequency_interval= models.CharField(max_length=30, choices=WaterSources,null=True)
    frequency_times = models.FloatField(default=0)
    frequency_interval= models.CharField(max_length=10, choices=FrequencyInterval,null=True)
    report_id = models.ForeignKey(
        WaterReport, on_delete=models.CASCADE, related_name="irrigations"
    )
    quantity = models.FloatField(default=0)
