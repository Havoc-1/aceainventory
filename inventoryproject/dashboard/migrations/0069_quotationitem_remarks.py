# Generated by Django 4.0.3 on 2023-07-03 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0068_quotationitem_isrejected'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotationitem',
            name='remarks',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
