# Generated by Django 4.0.3 on 2022-05-10 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_alter_inventory_type'),
        ('delivery', '0006_remove_deliveryitem_inventory_content_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliveryitem',
            name='inventory',
        ),
        migrations.AddField(
            model_name='deliveryitem',
            name='inventory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.inventory'),
        ),
    ]
