from django.contrib import admin
from .models import UnderrepresentedGroup

@admin.register(UnderrepresentedGroup)
class UnderrepresentedGroupsNameAdmin(admin.ModelAdmin):
    list_display = ("name",)
