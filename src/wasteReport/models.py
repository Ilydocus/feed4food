from django.db import models
from django.contrib.auth.models import User

class WasteAction(models.Model):
    name = models.CharField(
        max_length=100, blank=False, null=False, unique=True, primary_key=True
    )

class WasteType(models.Model):
    name = models.CharField(
        max_length=100, blank=False, null=False, unique=True, primary_key=True
    )
    unit = models.CharField(max_length=100, blank=False, null=False)


class WasteReport(models.Model):
    report_id = models.AutoField(blank=False, null=False, unique=True, primary_key=True)

    start_date = models.DateField()
    end_date = models.DateField()
    creation_time = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    city = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    garden = models.CharField(max_length=100)



class WasteReportDetails(models.Model):
    wasteType = models.ForeignKey(WasteType, on_delete=models.CASCADE)
    wasteAction = models.ForeignKey(WasteAction, on_delete=models.CASCADE)
    report_id = models.ForeignKey(
        WasteReport, on_delete=models.CASCADE, related_name="details"
    )
    quantity = models.FloatField()



