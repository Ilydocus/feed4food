# Create your models here.
from django.contrib.gis.db import models
from django.contrib.auth.models import User

class Items(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True, primary_key=True)
    latin_name = models.CharField(max_length=100, blank=True, null=True)
    locale = models.BooleanField()
    unit = models.CharField(max_length=100, blank=False, null=False)

class ProduceReport(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    timestamp = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.PointField(geography=True, null=True, blank=True)  # Stores geolocation

class ProduceReportDetails(models.Model):
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    report = models.ForeignKey(ProduceReport, on_delete=models.CASCADE)
    quantity = models.FloatField()

