# Generated by Django 4.0.3 on 2023-02-03 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0027_delivery_remove_deliveryitem_deliverydetails_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='delivery',
            old_name='date',
            new_name='dateRequested',
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='approved',
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='arrived',
        ),
        migrations.AddField(
            model_name='delivery',
            name='dateApproved',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='delivery',
            name='dateArrived',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]