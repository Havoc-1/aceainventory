# Generated by Django 4.0.3 on 2022-11-07 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0018_alter_stock_options_inventory'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Inventory',
        ),
    ]
