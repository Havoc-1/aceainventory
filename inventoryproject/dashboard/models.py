from django.db import models
from django.contrib.auth.models import Group, User
from django.utils.text import slugify
from django.conf import settings

# Create your models here.

admin_group= Group.objects.get_or_create(name='Administrator')
management_group= Group.objects.get_or_create(name='Management')
finance_group = Group.objects.get_or_create(name='Finance')
engineering_group = Group.objects.get_or_create(name='Engineering')

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

class Inventory(models.Model):
    name = models.CharField(max_length=100, null=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)     
    quantity = models.PositiveIntegerField(null=True)

    class Meta:
        constraints = [
                models.UniqueConstraint(fields=["name", "location"], name='Location Instance'),
        ]
        verbose_name_plural = 'Inventory Items'
    
    def __str__(self):                                                      # function returning the data models to string
        return f'{self.name} - {self.location}'  


# ==================================== PURCHASE REQUEST MODELS ======================================================= #


class PurchaseRequest(models.Model):
    requestedBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    approvedBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='approved_requests',null=True, blank=True)
    dateRequested = models.DateTimeField(auto_now_add=True, blank=True)
    dateApproved = models.DateTimeField(null=True, blank=True)
    approvedQuotations = models.BooleanField(default=False)
    approvedDelivery = models.BooleanField(default=False)
    requestLocation = models.ForeignKey(Location, on_delete=models.CASCADE)

    class Meta:                                                             # django admin data models are pluralized (they add 's')
        verbose_name_plural = 'Purchase Requests'
    
    def __str__(self):
        if self.requestedBy:
            initials = ''.join([name[0] for name in self.requestedBy.get_full_name().split()])
        else:
            initials = 'unknown'
        formatted_date = self.dateRequested.strftime('%d%b%y')
        slug = slugify(formatted_date).upper()
        return f'{initials}-{slug}'

class PurchaseRequestItem(models.Model):
    purchaseRequest = models.ForeignKey(PurchaseRequest, on_delete=models.CASCADE, related_name='purchase_request_items')
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(null=True)

    class Meta:                                                             # django admin data models are pluralized (they add 's')
        verbose_name_plural = 'Purchase Request Items'

    def __str__(self):                                                      # function returning the data models to string
        return f'{self.purchaseRequest} - {self.inventory.name} - {self.quantity}'               # arrangement and data values here would need to be reflected under dashboard/admin.py under Inventory model
    


# ==================================== QUOTATION MODELS ======================================================= #


class Quotation(models.Model):
    id = models.AutoField(primary_key=True)
    purchaseRequest = models.ForeignKey(PurchaseRequest, on_delete=models.CASCADE,null=True, blank=True)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_quotations')
    dateCreated = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:                                                             # django admin data models are pluralized (they add 's')
        verbose_name_plural = 'Quotations'
    

class QuotationItem(models.Model):
    id = models.AutoField(primary_key=True)
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, null=True)
    approvedBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='approved_quotations',null=True, blank=True)
    dateApproved = models.DateTimeField(null=True, blank=True)
    supplierName = models.CharField(max_length=100, null=True)
    deliverySet = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(null=True)
    price = models.PositiveIntegerField(null=True)

    class Meta:                                                             # django admin data models are pluralized (they add 's')
        verbose_name_plural = 'Quotation Items'


# ==================================== DELIVERY MODELS ======================================================= #
    

class DeliveryItem(models.Model):
    id = models.AutoField(primary_key=True)
    quotationItem = models.ForeignKey(QuotationItem, on_delete=models.CASCADE, null=True)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, null=True)
    deliveryLocation = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    approvedBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True)
    dateApproved = models.DateTimeField(null=True, blank=True)
    expectedDeliveryDate = models.DateTimeField(null=True, blank=True)
    dateArrived = models.DateTimeField(null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True)

    class Meta:                                                             # django admin data models are pluralized (they add 's')
        verbose_name_plural = 'Delivery Items'