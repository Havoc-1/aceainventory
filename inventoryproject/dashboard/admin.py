from django.contrib import admin
from .models import Equipment, Deliveries
from django.contrib.auth.models import Group

admin.site.site_header = 'ACEA Inventory Admin Dashboard'

class EquipAdmin(admin.ModelAdmin):                     
    list_display = ('name', 'location', 'status',)      # displays the equipment model with the following list
    list_filter = ['type']                              # can filter by type ()

# Register your models here.
admin.site.register(Equipment, EquipAdmin)
admin.site.register(Deliveries)