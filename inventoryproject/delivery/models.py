from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
STATUS = (                                    # creation of types to display as choices (STILL INCOMPLETE)
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
)

class DeliveryItem(models.Model):
    name = models.CharField(max_length=100, null=True)     
    quantity = models.PositiveIntegerField(null=True)
    specifications = models.CharField(max_length=100, null=True)    

    def __str__(self):                                                      # function returning the data models to string
        return f'{self.name} -- {self.quantity} -- {self.specifications}'         # arrangement and data values here would need to be reflected under dashboard/admin.py under Deliveries model

class Delivery(models.Model):
    inventory_item = models.ManyToManyField(DeliveryItem)               # ManyToMany since theres a lot
    staff = models.ForeignKey(User, models.CASCADE, null=True)
    status = models.CharField(max_length=100, choices=STATUS, null=True) 
    arrived = models.BooleanField(default=False)
    remarks = models.CharField(max_length=100, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:                                                             # django admin data models are pluralized (they add 's')
        verbose_name_plural = 'Deliveries'                                  # makes it gramatically correct
    
    def get_inventory_items(self):
        items = ''
        ct = 0
        print(self.inventory_item.all())
        for inventory in self.inventory_item.all():
            ct += 1
            items = items + str(ct) + '. ' + inventory.name + ' - ' + str(inventory.quantity) + '\n'

        return items[:-1]

    def __str__(self):                                                      # function returning the data models to string
        return f'Delivery number {self.id} ordered by {self.staff.username}'         # arrangement and data values here would need to be reflected under dashboard/admin.py under Deliveries model

