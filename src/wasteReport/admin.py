from django.contrib import admin
from .models import WasteAction, WasteType

@admin.register(WasteAction)
class WasteActionNameAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(WasteType)
class WasteTypeNameAdmin(admin.ModelAdmin):
    list_display = ("name",)

