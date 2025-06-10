from core import reportUtils
from django.db import models
from django.contrib.auth.models import User
from demographicReport.models import UnderrepresentedGroup



class EventReport(models.Model):
    class EventLocationOptions(models.TextChoices):
        LL = 'LL', 'At the LL location'
        ext = 'EXT', 'Outside of the LL'
    class EventTypeOptions(models.TextChoices):
        train = 'Training', 'Training'
        awa = 'Awareness', 'Awareness'
        oth = 'Other', 'Other'

    report_id = models.AutoField(blank=False, null=False, unique=True, primary_key=True)

    creation_time = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    city = models.CharField(max_length=100, choices=reportUtils.PartnerCities)

    event_date = models.DateField()
    event_name = models.CharField(max_length=100,default="")
    event_loc = models.CharField(max_length=100,choices=EventLocationOptions)
    event_type = models.CharField(max_length=100,choices=EventTypeOptions)
    event_desc = models.CharField(max_length=500,default="")
    
    #Participants
    total_invited = models.IntegerField(default=0)
    #Underrepresented groups as separate class
    total_participants = models.IntegerField(default=0)
    #Underrepresented groups as separate class

    #Economic 
    currency = models.CharField(max_length=3, choices=reportUtils.AvailableCurrency, default='EUR')
    event_costs = models.FloatField(default=0)
    event_costs_desc = models.CharField(max_length=500,default="", blank=True)
    event_revenues = models.FloatField(default=0)
    event_revenues_desc = models.CharField(max_length=500,default="", blank=True)

class EventPersonDetails(models.Model):
    name = models.ForeignKey(UnderrepresentedGroup, on_delete=models.CASCADE)
    report_id = models.ForeignKey(
        EventReport, on_delete=models.CASCADE, related_name="invited"
    )
    number_invited = models.IntegerField()
    number_participant = models.IntegerField()



    

    

