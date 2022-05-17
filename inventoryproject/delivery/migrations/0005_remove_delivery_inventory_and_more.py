# Generated by Django 4.0.3 on 2022-05-10 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0004_deliveryitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delivery',
            name='inventory',
        ),
        migrations.RemoveField(
            model_name='deliveryitem',
            name='delivery',
        ),
        migrations.AddField(
            model_name='delivery',
            name='inventory_item',
            field=models.ManyToManyField(to='delivery.deliveryitem'),
        ),
    ]