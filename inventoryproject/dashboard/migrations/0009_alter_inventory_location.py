# Generated by Django 4.0.3 on 2022-05-15 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_brand_location_alter_inventory_brand_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='location',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.location'),
        ),
    ]
