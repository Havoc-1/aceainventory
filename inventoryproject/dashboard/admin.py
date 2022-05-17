from django.contrib import admin
from .models import Inventory, Location, Brand, Type
from django.contrib.auth.models import Group

admin.site.site_header = 'ACEA Inventory Admin Dashboard'

class InventoryAdmin(admin.ModelAdmin):                     
    list_display = ('name', 'location', 'quantity', 'status',)      # displays the inventory model with the following list
    list_filter = ['type']                              # can filter by type ()

# Register your models here.
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Location)
admin.site.register(Brand)
admin.site.register(Type)