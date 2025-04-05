# Generated by Django 3.2.25 on 2025-04-04 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0013_auto_20250404_1856'),
    ]

    operations = [

        migrations.AddField(
            model_name='flat',
            name='owners',
            field=models.ManyToManyField(related_name='owned_flats', through='property.FlatOwnership', to='property.Owner'),
        ),
    ]
