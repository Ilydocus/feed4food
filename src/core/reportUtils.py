from django.db import models
from django.contrib.auth.models import User

class PartnerCities(models.TextChoices):
        Bucharest = 'Bucharest', 'Bucharest'
        Drama = 'Drama', 'Drama'
        Strovolos = 'Strovolos', 'Strovolos'
        Amsterdam = 'Amsterdam', 'Amsterdam'

class AvailableCurrency(models.TextChoices):
        EUR = 'EUR', '€'
        RON = 'RON', 'lei'