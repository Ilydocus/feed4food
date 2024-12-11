from django.contrib import admin
# from .models import ProduceReport

# admin.site.register(ProduceReport)


from .models import Item, ItemDetail

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'requires_details')

@admin.register(ItemDetail)
class ItemDetailAdmin(admin.ModelAdmin):
    list_display = ('item', 'key', 'value', 'quantity')