from django.db import models
from django.contrib.auth.models import Group, User
from django.utils.text import slugify
import datetime

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

class Supplier(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SupplierItem(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='items')
    inventory_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    dateApproved = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.inventory_name} ({self.supplier})"

class Inventory(models.Model):
    name = models.CharField(max_length=100, null=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)     
    quantity = models.PositiveIntegerField(null=True)
    restocking_threshold = models.PositiveIntegerField(null=True)
    restocking_amount = models.PositiveIntegerField(null=True)

    class Meta:
        constraints = [
                models.UniqueConstraint(fields=["name", "location"], name='Location Instance'),
        ]
        verbose_name_plural = 'Inventory Items'
    
    def __str__(self):                                                      # function returning the data models to string
        return f'{self.name} - {self.location}'  

class InventoryWithdrawn(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, null=True)     
    quantity = models.PositiveIntegerField(null=True)
    withdrawn_by = models.ForeignKey(User, on_delete=models.CASCADE)
    withdrawn_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Withdrawn Inventory Items'
    
    def __str__(self):                                                      # function returning the data models to string
        return f'{self.inventory} - {self.quantity}'  

class InventoryDamaged(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, null=True)     
    location = models.ForeignKey(Location, on_delete=models.CASCADE)     
    quantity = models.PositiveIntegerField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    verified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='damage_verify_person', null=True, blank=True,)
    reported_date = models.DateTimeField(auto_now_add=True)
    verified_date = models.DateTimeField(null=True, blank=True)
    remarks = models.CharField(max_length=1000, blank=True)

    class Meta:
        verbose_name_plural = 'Damaged Inventory Items'
    
    def __str__(self):                                                      # function returning the data models to string
        return f'{self.inventory} - {self.quantity}'  
    
class InventoryReturned(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, null=True)     
    quantity = models.PositiveIntegerField(null=True)
    transferred_by = models.ForeignKey(User, on_delete=models.CASCADE)
    received_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_inventory_person', null=True, blank=True)
    transferredFrom = models.ForeignKey(Location, on_delete=models.CASCADE)
    transferredTo = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='received_inventory_location', null=True, blank=True)
    transferDate = models.DateTimeField(auto_now_add=True)
    arrivalDate = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Transferred Inventory Items'
    
    def __str__(self):                                                      # function returning the data models to string
        return f'{self.inventory} - {self.quantity}'  

class InventoryRecount(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, null=True)     
    oQuantity = models.PositiveIntegerField(null=True)
    rQuantity = models.PositiveIntegerField(null=True)
    recounted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    recountDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Recounted Inventory Log'
    
    def __str__(self):                                                      # function returning the data models to string
        return f'{self.inventory} - {self.rQuantity}'  
# ==================================== PURCHASE REQUEST MODELS ======================================================= #


class PurchaseRequest(models.Model):
    requestedBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    approvedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approved_requests',null=True, blank=True)
    dateRequested = models.DateTimeField(auto_now_add=True, blank=True)
    dateApproved = models.DateTimeField(null=True, blank=True)
    approvedQuotations = models.BooleanField(default=False)
    approvedDelivery = models.BooleanField(default=False)
    requestLocation = models.ForeignKey(Location, on_delete=models.CASCADE)
    confirmedDeliveryCount = models.PositiveIntegerField(null=True, default=0)
    totalDeliveryCount = models.PositiveIntegerField(null=True, default=0)

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
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_quotations')
    dateCreated = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:                                                             # django admin data models are pluralized (they add 's')
        verbose_name_plural = 'Quotations'
    

class QuotationItem(models.Model):
    id = models.AutoField(primary_key=True)
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, null=True)
    approvedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approved_quotations',null=True, blank=True)
    isRejected = models.BooleanField(default=False)
    dateApproved = models.DateTimeField(null=True, blank=True)
    supplierName = models.CharField(max_length=100, null=True)
    methodOfPayment = models.CharField(max_length=100, null=True)
    deliverySet = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(null=True)
    pricePerUnit = models.PositiveIntegerField(blank=True, null=True)
    totalPrice = models.PositiveIntegerField(blank=True, null=True)
    remarks = models.CharField(max_length=1000, blank=True)

    class Meta:                                                             # django admin data models are pluralized (they add 's')
        verbose_name_plural = 'Quotation Items'
    
    def __str__(self):
        if self.approvedBy:
            initials = ''.join([name[0] for name in self.quotation.createdBy.get_full_name().split()])
        else:
            initials = 'unknown'
        formatted_date = self.quotation.purchaseRequest.dateRequested.strftime('%d%b%y')
        slug = slugify(formatted_date).upper()
        return f'{initials}-{slug}'

# ==================================== DELIVERY MODELS ======================================================= #
    

class DeliveryItem(models.Model):
    id = models.AutoField(primary_key=True)
    quotationItem = models.ForeignKey(QuotationItem, on_delete=models.CASCADE, null=True)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, null=True)
    deliveryLocation = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    approvedBy = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    dateApproved = models.DateTimeField(null=True, blank=True)
    expectedDeliveryDate = models.DateTimeField(null=True, blank=True)
    dateArrived = models.DateTimeField(null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True)
    pQuantity = models.PositiveIntegerField(null=True, default=0)

    @property
    def status(self):
        if self.dateArrived is None:
            if self.dateApproved is None:
                return 'Approval Pending'
            elif self.expectedDeliveryDate and self.expectedDeliveryDate < datetime.datetime.now(datetime.timezone.utc):
                late_days = (datetime.datetime.now(datetime.timezone.utc) - self.expectedDeliveryDate).days
                return f'Arrival Late by {late_days} day/s'
            else:
                return 'Awaiting Delivery'
        else:
            return 'Delivered'

    class Meta:                                                             # django admin data models are pluralized (they add 's')
        verbose_name_plural = 'Delivery Items'

    def __str__(self):                                                      # function returning the data models to string
        quantity = self.pQuantity if self.pQuantity is not None and self.pQuantity > 0 else self.quantity
        return f'00{self.quotationItem.quotation.id}: {self.inventory.name} - {quantity}'