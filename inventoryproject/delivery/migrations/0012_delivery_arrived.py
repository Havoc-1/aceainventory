# Generated by Django 4.0.3 on 2022-05-17 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0011_alter_delivery_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='arrived',
            field=models.BooleanField(default=False),
        ),
    ]