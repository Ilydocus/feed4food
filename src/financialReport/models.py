from django.db import models
from django.contrib.auth.models import User


class FinancialReport(models.Model):
    report_id = models.AutoField(blank=False, null=False, unique=True, primary_key=True)

    start_date = models.DateField()
    end_date = models.DateField()
    creation_time = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    city = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    garden = models.CharField(max_length=100)

    #Expenses
    exp_workforce = models.FloatField()
    exp_purchase = models.FloatField()
    exp_others = models.FloatField()
    exp_others_desc = models.CharField(max_length=500)

    #Funding
    fun_feed4food = models.FloatField()
    fun_others = models.FloatField()
    fun_others_desc = models.CharField(max_length=500)

    #Revenues
    rev_production = models.FloatField()
    rev_restaurant = models.FloatField()
    rev_events = models.FloatField()
    rev_others = models.FloatField()
    rev_others_desc = models.CharField(max_length=500)

