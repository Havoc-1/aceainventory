# Generated by Django 4.0.3 on 2023-07-03 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0070_alter_quotationitem_priceperunit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotationitem',
            name='quantity',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='quotationitem',
            name='totalPrice',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]