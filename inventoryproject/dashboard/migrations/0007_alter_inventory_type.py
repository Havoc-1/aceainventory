# Generated by Django 4.0.3 on 2022-04-21 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_alter_inventory_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='type',
            field=models.CharField(choices=[('Consummable', 'Consummable'), ('ConstructionSupply', 'ConstructionSupply'), ('DefBars', 'DefBars'), ('Electrical', 'Electrical'), ('Paint', 'Paint'), ('Scrap', 'Scrap'), ('Tools', 'Tools'), ('Uniform', 'Uniform')], max_length=100, null=True),
        ),
    ]
