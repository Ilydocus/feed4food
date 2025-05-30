from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductNameAdmin(admin.ModelAdmin):
    list_display = ("name",)
