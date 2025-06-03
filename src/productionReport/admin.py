from django.contrib import admin
from .models import Product, LLLocation


@admin.register(Product)
class ProductNameAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(LLLocation)
class LocationNameAdmin(admin.ModelAdmin):
    list_display = ("name",)
