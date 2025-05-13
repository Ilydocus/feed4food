from django.db import models
from django.contrib.auth.models import User
from report.models import Item

class SalesReport(models.Model):
    report_id = models.AutoField(blank=False, null=False, unique=True, primary_key=True)

    creation_time = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    city = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    garden = models.CharField(max_length=100)


class SalesReportDetails(models.Model):
    class AvailableCurrency(models.TextChoices):
        EUR = 'EUR'
        RON = 'RON'
    sale_date = models.DateField()
    sale_location = models.CharField(max_length=100)
    product = models.ForeignKey(Item, on_delete=models.CASCADE) 
    report_id = models.ForeignKey(
        SalesReport, on_delete=models.CASCADE, related_name="details"
    )
    quantity = models.FloatField()
    price = models.FloatField()
    currency = models.CharField(max_length=3, choices=AvailableCurrency, default='EUR')
