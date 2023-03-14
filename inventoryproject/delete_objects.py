import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventoryproject.settings')
import django
django.setup()

from dashboard.models import PurchaseRequest

PurchaseRequest.objects.all().delete()