# Generated by Django 4.0.3 on 2023-03-13 07:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0037_alter_quotation_id_alter_quotationitem_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryItems',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('supplierName', models.CharField(max_length=100, null=True)),
                ('dateApproved', models.DateTimeField(blank=True, null=True)),
                ('quantity', models.PositiveIntegerField(null=True)),
                ('approvedBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Quotation Items',
            },
        ),
        migrations.CreateModel(
            name='PurchaseRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateRequested', models.DateTimeField(auto_now_add=True)),
                ('dateApproved', models.DateTimeField(blank=True, null=True)),
                ('approvedBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approved_requests', to=settings.AUTH_USER_MODEL)),
                ('requestLocation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.location')),
                ('requestedBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Purchase Requests',
            },
        ),
        migrations.CreateModel(
            name='PurchaseRequestItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(null=True)),
                ('inventory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.inventory')),
                ('purchaseRequest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.purchaserequest')),
            ],
            options={
                'verbose_name_plural': 'Purchase Request Items',
            },
        ),
        migrations.AlterModelOptions(
            name='delivery',
            options={'verbose_name_plural': 'Quotations'},
        ),
        migrations.RenameField(
            model_name='delivery',
            old_name='dateRequested',
            new_name='dateCreated',
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='dateApproved',
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='dateArrived',
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='requestedBy',
        ),
        migrations.RemoveField(
            model_name='quotation',
            name='approvedBy',
        ),
        migrations.RemoveField(
            model_name='quotation',
            name='dateApproved',
        ),
        migrations.RemoveField(
            model_name='quotation',
            name='delivery',
        ),
        migrations.RemoveField(
            model_name='quotation',
            name='supplierName',
        ),
        migrations.AddField(
            model_name='delivery',
            name='createdBy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='quotationitem',
            name='approvedBy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approved_quotations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='quotationitem',
            name='dateApproved',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='quotationitem',
            name='supplierName',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.DeleteModel(
            name='DeliveryItem',
        ),
        migrations.AddField(
            model_name='deliveryitems',
            name='delivery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.delivery'),
        ),
        migrations.AddField(
            model_name='deliveryitems',
            name='inventory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.inventory'),
        ),
        migrations.AddField(
            model_name='quotation',
            name='purchaseRequest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.purchaserequest'),
        ),
    ]
