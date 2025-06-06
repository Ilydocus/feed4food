from django.db import models
from django.contrib.auth.models import User
from productionReport.models import Product, LLLocation, Garden
from core import reportUtils

class SalesReport(models.Model):
    
    report_id = models.AutoField(blank=False, null=False, unique=True, primary_key=True)

    creation_time = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    city = models.CharField(max_length=100, choices=reportUtils.PartnerCities)
    location = models.ForeignKey(LLLocation, on_delete=models.SET_NULL, null=True)
    garden = models.ForeignKey(Garden, on_delete=models.SET_NULL, null=True)
    currency = models.CharField(max_length=3, choices=reportUtils.AvailableCurrency, default='EUR')


class SalesReportDetails(models.Model):
    
    sale_date = models.DateField()
    sale_location = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    report_id = models.ForeignKey(
        SalesReport, on_delete=models.CASCADE, related_name="details"
    )
    quantity = models.FloatField()
    price = models.FloatField()
    
