import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventoryproject.settings')
django.setup()

from dashboard.models import PurchaseRequestItem, PurchaseRequest

PurchaseRequest.objects.all().delete()
PurchaseRequestItem.objects.all().delete()
