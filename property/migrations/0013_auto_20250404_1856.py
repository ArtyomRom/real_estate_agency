from django.db import migrations, models
import django.db.models.deletion
from django.db import migrations, models


def populate_ownership(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')
    Owner = apps.get_model('property', 'Owner')
    FlatOwnership = apps.get_model('property', 'FlatOwnership')

    # Пройдем по всем квартирам и создадим связи владельцев
    for flat in Flat.objects.all():
        # Предположим, что у вас есть поле owner в модели Flat, или список владельцев
        # Например, если у нас в поле owner несколько владельцев:
        for owner in flat.owners.all():  # Получаем владельцев квартиры
            # Создаем запись в промежуточной модели FlatOwnership
            FlatOwnership.objects.get_or_create(flat=flat, owner=owner)


class Migration(migrations.Migration):
    dependencies = [
        ('property', '0012_auto_20250403_2323'),
    ]

    operations = [
        # Создание модели FlatOwnership, если ее еще нет
        migrations.CreateModel(
            name='FlatOwnership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ownership_owners',
                                           to='property.flat')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ownerships',
                                            to='property.owner')),
            ],
            options={
                'unique_together': {('owner', 'flat')},
            },
        ),

        # Создаем связь ManyToMany через FlatOwnership
        migrations.AddField(
            model_name='flat',
            name='owners',
            field=models.ManyToManyField(
                related_name='owned_flats',
                through='property.FlatOwnership',
                to='property.Owner',
            ),
        ),

        # Заполняем таблицу FlatOwnership данными
        migrations.RunPython(populate_ownership),
    ]
