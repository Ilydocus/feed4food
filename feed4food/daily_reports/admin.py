from django.contrib import admin
from .models import ItemName
@admin.register(ItemName)
class ItemNameAdmin(admin.ModelAdmin):
    list_display = ('name',)