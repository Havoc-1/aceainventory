# Generated by Django 4.0.3 on 2022-05-05 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='delivery',
            old_name='delivery_quantity',
            new_name='quantity',
        ),
    ]
