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

class CultivationTypes(models.TextChoices):
        Surface = 'Surface', 'm^2'
        NbPlants = 'NbPlants', 'plants'

def get_label_of_choice_class(choices_class, value):
    return dict(choices_class.choices).get(value)

class InputType(models.TextChoices):
        Fertilizer = 'Fertilizer', 'Fertilizer'
        Pesticide = 'Pesticide', 'Pesticide'
        Other = 'Other', 'Other'
        
class InputCategory(models.TextChoices):
        Natural = 'Natural', 'Natural'
        Synthetic = 'Synthetic', 'Synthetic'
        Other = 'Other', 'Other'

class NutrientColors(models.TextChoices):
        BluePurple = 'Blue/Purple', 'Blue/Purple'
        Red = 'Red', 'Red'
        YellowOrange = 'Yellow/Orange', 'Yellow/Orange'
        White = 'White', 'White'
        Green = 'Green', 'Green'