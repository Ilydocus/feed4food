from django.contrib import admin
from .models import Item


@admin.register(Item)
class ItemNameAdmin(admin.ModelAdmin):
    list_display = ("name",)
