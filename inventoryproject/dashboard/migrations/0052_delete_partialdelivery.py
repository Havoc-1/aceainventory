# Generated by Django 4.0.3 on 2023-05-29 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0051_deliveryitem_ispartial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PartialDelivery',
        ),
    ]
