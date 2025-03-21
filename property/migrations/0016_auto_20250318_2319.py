# Generated by Django 5.1.7 on 2025-03-18 20:19

from django.db import migrations

def load_owners(apps, schema_editor):
    flat_apartament = apps.get_model('property', 'Flat')
    owner = apps.get_model('property', 'Owner')

    for apartament in flat_apartament.objects.all():
        # Находим все квартиры с таким же владельцем и телефоном
        related_apartaments = flat_apartament.objects.filter(
            owner=apartament.owner,
            owner_pure_phone=apartament.owner_pure_phone
        )

        # Создаем или получаем владельца с учетом данных
        owner_instance, created = owner.objects.get_or_create(
            owner=apartament.owner,
            owner_correct_phone=apartament.owner_pure_phone,
            defaults={'owner_number': apartament.owners_phonenumber}
        )

        # Привязываем все найденные квартиры к владельцу
        owner_instance.apartaments.set(related_apartaments)


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0013_alter_owner_apartaments'),
    ]

    operations = [
        migrations.RunPython(load_owners)
    ]
