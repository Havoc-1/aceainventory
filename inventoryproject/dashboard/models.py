from django.db import models
from django.contrib.auth.models import User

# Create your models here.
TYPE = (                                    # creation of types to display as choices (STILL INCOMPLETE)
    ('DefBars', 'DefBars'),
    ('Tools', 'Tools'),
)

class Equipment(models.Model):                                              # django does most of the hardwork, so follow the template (CharField for strings, PositiveIntegerField for int)
    name = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=100, choices=TYPE, null=True)        
    brand = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True)
    quantity = models.PositiveIntegerField(null=True)
    remarks = models.CharField(max_length=100, null=True)

    def __str__(self):                                                      # function returning the data models to string
        return f'{self.name}--{self.location}--{self.status}'               # arrangement and data values here would need to be reflected under dashboard/admin.py under Equipment model

class Deliveries(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, null=True)       # CASCADE - done so that when the referenced object is deleted, all objects referencing it would be deleted too
    staff = models.ForeignKey(User, models.CASCADE, null=True)
    delivery_quantity = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:                                                             # django admin data models are pluralized (they add 's')
        verbose_name_plural = 'Deliveries'                                  # makes it gramatically correct

    def __str__(self):                                                      # function returning the data models to string
        return f'{self.equipment} ordered by {self.staff.username}'         # arrangement and data values here would need to be reflected under dashboard/admin.py under Deliveries model