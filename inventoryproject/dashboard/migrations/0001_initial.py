# Generated by Django 4.0.3 on 2022-04-14 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('location', models.CharField(max_length=100, null=True)),
                ('type', models.CharField(choices=[('DefBars', 'DefBars'), ('Tools', 'Tools')], max_length=100, null=True)),
                ('brand', models.CharField(max_length=100, null=True)),
                ('status', models.CharField(max_length=100, null=True)),
                ('quantity', models.PositiveIntegerField(null=True)),
                ('remarks', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]