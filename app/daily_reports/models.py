# Create your models here.
from django.db import models

class ProduceReport(models.Model):
    farmer_name = models.CharField(max_length=100)
    produce_type = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    date_submitted = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.farmer_name} - {self.produce_type}"

class Item(models.Model):
    name = models.CharField(max_length=255)  # E.g., "Apple", "Banana"
    requires_details = models.BooleanField(default=False)  # Flag if extra details are needed

    def __str__(self):
        return self.name  # This will display the name in dropdowns

class ItemDetail(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    key = models.CharField(max_length=255)  # E.g., "Breed"
    value = models.CharField(max_length=255)  # E.g., "Red Delicious"
    quantity = models.PositiveIntegerField(default=0)
