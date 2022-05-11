from django.contrib import admin
from .models import Delivery, DeliveryItem
from django.contrib.auth.models import Group

# Register your models here.
class DeliveryAdmin(admin.ModelAdmin):                     
    list_display = ('inventory_name', 'quantity')      # displays the delivery item model with the following list
    # list_filter = ['inventory__type']                # commented out 'til I could figure out what to do with this

    @admin.display(description='Name')
    def inventory_name(self, obj):
        return obj.inventory.name

    # @admin.display(description='Quantity')
    # def inventory_quantity(self, object):
    #     return object.inventory.quantity
    
    # @admin.display(description='Type')
    # def inventory_type(self, object):
    #     return object.inventory.type


admin.site.register(Delivery)
admin.site.register(DeliveryItem, DeliveryAdmin)

