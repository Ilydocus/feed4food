from django.db import models
from django.contrib.auth.models import User


class FinancialReport(models.Model):
    class AvailableCurrency(models.TextChoices):
        EUR = 'EUR'
        RON = 'RON'
    
    report_id = models.AutoField(blank=False, null=False, unique=True, primary_key=True)

    start_date = models.DateField()
    end_date = models.DateField()
    creation_time = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    currency = models.CharField(max_length=3, choices=AvailableCurrency, default='EUR')

    city = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    garden = models.CharField(max_length=100)

    #Expenses
    exp_workforce = models.FloatField(default=0)
    exp_purchase = models.FloatField(default=0)
    exp_others = models.FloatField(default=0)
    exp_others_desc = models.CharField(max_length=500,default="", blank=True)

    #Funding
    fun_feed4food = models.FloatField(default=0)
    fun_others = models.FloatField(default=0)
    fun_others_desc = models.CharField(max_length=500,default="", blank=True)

    #Revenues
    #rev_production = models.FloatField(default=0)
    rev_restaurant = models.FloatField(default=0)
    #rev_events = models.FloatField(default=0)
    rev_others = models.FloatField(default=0)
    rev_others_desc = models.CharField(max_length=500,default="", blank=True)

