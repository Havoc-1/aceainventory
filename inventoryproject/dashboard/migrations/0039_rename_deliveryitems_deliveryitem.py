# Generated by Django 4.0.3 on 2023-03-13 07:08

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0038_deliveryitems_purchaserequest_purchaserequestitem_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DeliveryItems',
            new_name='DeliveryItem',
        ),
    ]
