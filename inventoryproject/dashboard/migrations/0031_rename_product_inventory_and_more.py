# Generated by Django 4.1.6 on 2023-02-16 06:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0030_rename_delivery_location_delivery_deliverylocation'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Product',
            new_name='Inventory',
        ),
        migrations.RenameField(
            model_name='deliveryitem',
            old_name='product',
            new_name='inventory',
        ),
    ]
