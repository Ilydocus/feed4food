from django.db import models
from django.contrib.auth.models import User

class WaterReport(models.Model):
    report_id = models.AutoField(blank=False, null=False, unique=True, primary_key=True)

    creation_time = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    city = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    garden = models.CharField(max_length=100)



class WaterReportRainfall(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    report_id = models.ForeignKey(
        WaterReport, on_delete=models.CASCADE, related_name="rainfall"
    )
    quantity = models.FloatField()

class WaterReportIrrigation(models.Model):
    class FrequencyInterval(models.TextChoices):
        DAY = 'day'
        WEEK = 'week'
        MONTH = 'month'
    start_date = models.DateField()
    end_date = models.DateField()
    period = models.BooleanField()
    frequency_times = models.FloatField()
    frequency_interval= models.CharField(max_length=10, choices=FrequencyInterval)
    report_id = models.ForeignKey(
        WaterReport, on_delete=models.CASCADE, related_name="irrigation"
    )
    quantity = models.FloatField()
