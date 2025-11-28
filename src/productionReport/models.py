from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from core import reportUtils

class ProductCategory(models.Model):
    name = models.CharField(
        max_length=100, blank=False, null=False, unique=True, primary_key=True
    )
    color = models.CharField(choices=reportUtils.NutrientColors, max_length=100, blank=True)
    
    energy_kcal = models.IntegerField(default=0)
    energy_kj = models.IntegerField(default=0)

    vitamin_a = models.FloatField(default=0)
    vitamin_d = models.FloatField(default=0)
    vitamin_e = models.FloatField(default=0)
    vitamin_k = models.FloatField(default=0)
    vitamin_c = models.FloatField(default=0)
    vitamin_b1 = models.FloatField(default=0)
    vitamin_b2 = models.FloatField(default=0)
    vitamin_b3 = models.FloatField(default=0)
    vitamin_b6 = models.FloatField(default=0)
    vitamin_b9 = models.FloatField(default=0)
    vitamin_b12 = models.FloatField(default=0)

    potassium = models.FloatField(default=0)
    calcium = models.FloatField(default=0)
    phosphorus = models.FloatField(default=0)
    magnesium = models.FloatField(default=0)
    iron = models.FloatField(default=0)
    zinc = models.FloatField(default=0)
    copper = models.FloatField(default=0)
    selenium = models.FloatField(default=0)
    iodine = models.FloatField(default=0)

    total_fat = models.FloatField(default=0)
    saturates = models.FloatField(default=0)
    carbohydrates = models.FloatField(default=0)
    sugars = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    salt = models.FloatField(default=0)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(
        max_length=100, blank=False, null=False, unique=True, primary_key=True
    )
    latin_name = models.CharField(max_length=100, blank=True, null=True)
    living_lab = models.CharField(choices=reportUtils.PartnerCities, max_length=100, blank=False)
    native_variety = models.BooleanField()
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True)
    unit = models.CharField(max_length=100, blank=False, null=False)
    cultivation_type = models.CharField(choices=reportUtils.CultivationTypes, max_length=100, blank=False, default=reportUtils.CultivationTypes.Surface)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class LLLocation(models.Model):
    name = models.CharField(
        max_length=100, blank=False, null=False, unique=True, primary_key=True
    )
    living_lab = models.CharField(choices=reportUtils.PartnerCities, max_length=100, blank=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class Garden(models.Model):
    name = models.CharField(
        max_length=100, blank=False, null=False, unique=True, primary_key=True
    )
    living_lab = models.CharField(choices=reportUtils.PartnerCities, max_length=100, blank=False)
    location = models.ForeignKey(LLLocation, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class ProductionReport(models.Model):
    report_id = models.AutoField(blank=False, null=False, unique=True, primary_key=True)

    creation_time = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    city = models.CharField(max_length=100, choices=reportUtils.PartnerCities)
    location = models.ForeignKey(LLLocation, on_delete=models.SET_NULL, null=True)
    garden = models.ForeignKey(Garden, on_delete=models.SET_NULL, null=True)

    production_date = models.DateField(null=True)


class ProductionReportDetails(models.Model):
    name = models.ForeignKey(Product, on_delete=models.CASCADE)
    report_id = models.ForeignKey(
        ProductionReport, on_delete=models.CASCADE, related_name="details"
    )
    quantity = models.FloatField()

