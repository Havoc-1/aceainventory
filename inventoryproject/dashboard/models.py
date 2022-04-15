from django.db import models
from django.contrib.auth.models import User

# Create your models here.
TYPE = (
    ('DefBars', 'DefBars'),
    ('Tools', 'Tools'),
)

class Equipment(models.Model):
    name = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=100, choices=TYPE, null=True)
    brand = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True)
    quantity = models.PositiveIntegerField(null=True)
    remarks = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'{self.name}--{self.location}--{self.status}'

class Deliveries(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, null=True)
    staff = models.ForeignKey(User, models.CASCADE, null=True)
    delivery_quantity = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Deliveries'

    def __str__(self):
        return f'{self.equipment} ordered by {self.staff.username}'