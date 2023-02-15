from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

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


# ==================================== DELIVERY MODELS ======================================================= #


class Delivery(models.Model):
    requestedBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    dateRequested = models.DateTimeField(auto_now_add=True, blank=True)
    dateApproved = models.DateTimeField(null=True, blank=True)
    dateArrived = models.DateTimeField(null=True, blank=True)
    deliveryLocation = models.ForeignKey(Location, on_delete=models.CASCADE)

    class Meta:                                                             # django admin data models are pluralized (they add 's')
        verbose_name_plural = 'Deliveries'

    def update_dateArrived(self, dateArrived):
        self.dateArrived = dateArrived
        self.save()

    def update_dateApproved(self, dateApproved):
        self.dateApproved = dateApproved
        self.save()
    
    def __str__(self):
        if self.requestedBy:
            initials = ''.join([name[0] for name in self.requestedBy.get_full_name().split()])
        else:
            initials = 'unknown'
        formatted_date = self.dateRequested.strftime('%d%b%y')
        slug = slugify(formatted_date).upper()
        return f'{initials}-{slug}'

class DeliveryItem(models.Model):
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(null=True)

    class Meta:                                                             # django admin data models are pluralized (they add 's')
        verbose_name_plural = 'Delivery Items'

    def __str__(self):                                                      # function returning the data models to string
        return f'{self.delivery} - {self.product.name} - {self.quantity}'               # arrangement and data values here would need to be reflected under dashboard/admin.py under Inventory model