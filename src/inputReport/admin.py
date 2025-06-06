from django.contrib import admin
from .models import Input


@admin.register(Input)
class InputNameAdmin(admin.ModelAdmin):
    list_display = ("name",)
