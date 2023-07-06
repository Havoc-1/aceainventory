# Generated by Django 4.0.3 on 2023-07-01 15:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0063_inventorydamaged_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventorydamaged',
            name='verified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='damage_verify_person', to=settings.AUTH_USER_MODEL),
        ),
    ]
