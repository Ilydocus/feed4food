from django.contrib import admin
from .models import WaterReport, WaterReportIrrigation, WaterReportRainfall
# Register your models here.
admin.site.register(WaterReport)
admin.site.register(WaterReportIrrigation)
admin.site.register(WaterReportRainfall)