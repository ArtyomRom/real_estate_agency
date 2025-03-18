# Generated by Django 5.1.7 on 2025-03-18 16:49

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0010_auto_20250318_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flat',
            name='owner_pure_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region='RU', verbose_name='Нормализованный номер владельца'),
        ),
    ]
