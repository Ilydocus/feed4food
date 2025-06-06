from django.contrib import admin
from .models import Product, LLLocation, Garden, ProductCategory


@admin.register(Product)
class ProductNameAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(LLLocation)
class LocationNameAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Garden)
class GardenNameAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(ProductCategory)
class ProductCategoryNameAdmin(admin.ModelAdmin):
    list_display = ("name",)
