# Generated by Django 4.0.3 on 2022-04-15 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_deliveries'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deliveries',
            options={'verbose_name_plural': 'Deliveries'},
        ),
        migrations.RenameField(
            model_name='deliveries',
            old_name='deliveries',
            new_name='equipment',
        ),
    ]
