# Generated by Django 4.0.3 on 2022-11-11 11:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0023_rename_deliveryid_stock_deliverydetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliverybatches',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]