# Generated by Django 4.0.3 on 2023-07-01 10:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0059_alter_deliveryitem_pquantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryitem',
            name='pQuantity',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='purchaserequest',
            name='confirmedDeliveryCount',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='purchaserequest',
            name='totalDeliveryCount',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.CreateModel(
            name='InventoryReturned',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(null=True)),
                ('transferDate', models.DateTimeField(auto_now_add=True)),
                ('arrivalDate', models.DateTimeField(blank=True, null=True)),
                ('inventory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.inventory')),
                ('received_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_inventory_person', to=settings.AUTH_USER_MODEL)),
                ('transferredFrom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.location')),
                ('transferredTo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_inventory_location', to='dashboard.location')),
                ('transferred_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Withdrawn Inventory Items',
            },
        ),
        migrations.CreateModel(
            name='InventoryDamaged',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(null=True)),
                ('reported_date', models.DateTimeField(auto_now_add=True)),
                ('verified_date', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('inventory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.inventory')),
                ('verified_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='verified_inventory', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Withdrawn Inventory Items',
            },
        ),
    ]
