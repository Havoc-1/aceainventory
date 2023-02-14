# Generated by Django 4.0.3 on 2022-11-07 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0016_rename_requested_inventory_approved'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('status', models.CharField(choices=[('Available', 'Available'), ('Unavailable', 'Unavailable'), ('NA', 'NA')], max_length=100, null=True)),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.brand')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.location')),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.type')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrived', models.BooleanField(default=False)),
                ('approved', models.BooleanField(default=False)),
                ('quantity', models.PositiveIntegerField(null=True)),
                ('remarks', models.CharField(max_length=100, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.product')),
            ],
            options={
                'verbose_name_plural': 'Inventory',
            },
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='location',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='type',
        ),
        migrations.DeleteModel(
            name='Deliveries',
        ),
        migrations.DeleteModel(
            name='Inventory',
        ),
    ]
