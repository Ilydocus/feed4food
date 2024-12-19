from django.contrib import admin
from .models import Items

@admin.register(Items)
class ItemNameAdmin(admin.ModelAdmin):
    list_display = ('name',)