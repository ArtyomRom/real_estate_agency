# Generated by Django 2.2.24 on 2025-03-16 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0004_auto_20250316_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flat',
            name='new_building',
            field=models.BooleanField(blank=True, choices=[(True, 'Да'), (False, 'Нет')], default=False, null=True, verbose_name='Новостройка'),
        ),
    ]
