# Generated by Django 4.0.3 on 2023-07-01 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0061_alter_inventorydamaged_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventorydamaged',
            name='remarks',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
