from django.contrib import admin
from .models import DeliveryItem, Product, Brand, Type, Location, Delivery
from django.contrib.auth.models import Group

admin.site.site_header = 'ACEA Inventory Admin Dashboard'

# Register your models here.
# try: 
admin.site.register(Location)
admin.site.register(Brand)
admin.site.register(Type)
admin.site.register(DeliveryItem)
admin.site.register(Product)
admin.site.register(Delivery)
# admin.site.unregister(DeliveryItem)
# except admin.sites.AlreadyRegisterd:
#     pass
