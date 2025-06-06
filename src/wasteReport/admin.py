from django.contrib import admin
from .models import WasteType

@admin.register(WasteType)
class WasteTypeNameAdmin(admin.ModelAdmin):
    list_display = ("name",)

