# Generated by Django 4.0.3 on 2023-03-14 06:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0040_alter_delivery_options_alter_deliveryitem_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliveryitem',
            name='delivery',
        ),
        migrations.AddField(
            model_name='deliveryitem',
            name='deliveryLocation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.location'),
        ),
        migrations.AddField(
            model_name='deliveryitem',
            name='expectedDeliveryDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='purchaserequestitem',
            name='purchaseRequest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_request_items', to='dashboard.purchaserequest'),
        ),
        migrations.DeleteModel(
            name='Delivery',
        ),
    ]