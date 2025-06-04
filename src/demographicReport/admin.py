from django.contrib import admin
from .models import UnderrepresentedGroups

@admin.register(UnderrepresentedGroups)
class UnderrepresentedGroupsNameAdmin(admin.ModelAdmin):
    list_display = ("name",)
