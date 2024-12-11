# Create your models here.
from django.db import models

class ProduceReport(models.Model):
    farmer_name = models.CharField(max_length=100)
    produce_type = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    date_submitted = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.farmer_name} - {self.produce_type}"
