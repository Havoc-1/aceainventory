from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Location(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):                                                      
        return f'{self.name}'

class Brand(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):                                                      
        return f'{self.name}'

class Type(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):                                                      
        return f'{self.name}'

class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)     
    quantity = models.PositiveIntegerField(null=True)

    class Meta:
        constraints = [
                models.UniqueConstraint(fields=["name", "location"], name='Location Instance'),
        ]
    
    def __str__(self):                                                      # function returning the data models to string
        return f'{self.name} - {self.location}'  

class Delivery(models.Model):
    # add ordered by user
    dateRequested = models.DateTimeField(auto_now_add=True, blank=True)
    dateApproved = models.DateTimeField(null=True, blank=True)
    dateArrived = models.DateTimeField(null=True, blank=True)
    delivery_location = models.ForeignKey(Location, on_delete=models.CASCADE)

    class Meta:                                                             # django admin data models are pluralized (they add 's')
        verbose_name_plural = 'Deliveries'

    def update_dateArrived(self, dateArrived):
        self.dateArrived = dateArrived
        self.save()

    def update_dateApproved(self, dateApproved):
        self.dateApproved = dateApproved
        self.save()

    def __str__(self):                                                      # function returning the data models to string
        return f'{self.arrived}--{self.approved}'

class DeliveryItem(models.Model):
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(null=True)

    class Meta:                                                             # django admin data models are pluralized (they add 's')
        verbose_name_plural = 'Delivery Items'

    def __str__(self):                                                      # function returning the data models to string
        return f'{self.product}--{self.quantity}'               # arrangement and data values here would need to be reflected under dashboard/admin.py under Inventory model