from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from dashboard.models import Inventory

# Create your models here.
class DeliveryItem(models.Model):
    inventory = models.ForeignKey(Inventory, models.CASCADE, null=True)      
    quantity = models.PositiveIntegerField(null=True)

    def __str__(self):                                                      # function returning the data models to string
        return f'{self.inventory.name} -- {self.quantity}'         # arrangement and data values here would need to be reflected under dashboard/admin.py under Deliveries model

class Delivery(models.Model):
    inventory_item = models.ManyToManyField(DeliveryItem)               # ManyToMany since theres a lot
    staff = models.ForeignKey(User, models.CASCADE, null=True)
    status = models.CharField(max_length=100, null=True)
    remarks = models.CharField(max_length=100, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:                                                             # django admin data models are pluralized (they add 's')
        verbose_name_plural = 'Deliveries'                                  # makes it gramatically correct
    
    def __str__(self):                                                      # function returning the data models to string
        return f'Delivery number {self.id} ordered by {self.staff.username}'         # arrangement and data values here would need to be reflected under dashboard/admin.py under Deliveries model

