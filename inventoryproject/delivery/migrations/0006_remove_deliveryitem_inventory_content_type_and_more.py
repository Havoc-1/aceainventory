# Generated by Django 4.0.3 on 2022-05-10 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_alter_inventory_type'),
        ('delivery', '0005_remove_delivery_inventory_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliveryitem',
            name='inventory_content_type',
        ),
        migrations.RemoveField(
            model_name='deliveryitem',
            name='inventory_object_id',
        ),
        migrations.AddField(
            model_name='deliveryitem',
            name='inventory',
            field=models.ManyToManyField(to='dashboard.inventory'),
        ),
    ]
