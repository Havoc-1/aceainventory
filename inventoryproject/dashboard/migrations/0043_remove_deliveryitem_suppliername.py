# Generated by Django 4.0.3 on 2023-03-14 06:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0042_deliveryitem_quotationitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliveryitem',
            name='supplierName',
        ),
    ]