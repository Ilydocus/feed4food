# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class ProduceReport(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class ItemName(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)

class ProduceItem(models.Model):
    report = models.ForeignKey(ProduceReport, on_delete=models.CASCADE, related_name="items")
    item_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)
    item_type = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.FloatField(blank=True, null=True)