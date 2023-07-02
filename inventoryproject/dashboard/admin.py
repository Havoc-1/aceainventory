from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group

admin.site.site_header = 'ACEA Inventory Admin Dashboard'

# Register your models here.
# try: 
admin.site.register(Location)
admin.site.register(Brand)
admin.site.register(Type)
admin.site.register(PurchaseRequestItem)
admin.site.register(Inventory)
admin.site.register(InventoryWithdrawn)
admin.site.register(PurchaseRequest)
admin.site.register(Quotation)
admin.site.register(QuotationItem)
admin.site.register(DeliveryItem)
admin.site.register(InventoryReturned)
admin.site.register(InventoryDamaged)
# admin.site.unregister(Delivery)
# except admin.sites.AlreadyRegisterd:
#     pass