# Generated by Django 4.0.3 on 2022-11-11 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0022_remove_deliverybatches_items_stock_deliveryid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stock',
            old_name='deliveryID',
            new_name='deliveryDetails',
        ),
    ]
