# Generated by Django 4.1.7 on 2023-05-10 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0048_inventory_restocking_amount_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="purchaserequest",
            name="confirmedDeliveryCount",
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name="purchaserequest",
            name="totalDeliveryCount",
            field=models.PositiveIntegerField(null=True),
        ),
    ]