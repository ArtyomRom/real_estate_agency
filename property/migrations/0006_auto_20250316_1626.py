
from django.db import migrations, models

def set_new_building(apps, schema_editor):
    # Получаем доступ к модели Flat, как она была в миграциях, без применения изменений
    Flat = apps.get_model('property', 'Flat')
    for flat in Flat.objects.all():
        # Устанавливаем значение new_building на основе construction_year
        flat.new_building = True if flat.construction_year >= 2015 else False
        flat.save()

class Migration(migrations.Migration):

    dependencies = [
        ('property', '0005_auto_20250316_1617'),
    ]

    operations = [
        # Добавляем новое поле new_building
        migrations.AddField(
            model_name='flat',
            name='new_building',
            field=models.BooleanField(blank=True, choices=[(True, 'Да'), (False, 'Нет')], default=False, verbose_name='Новостройка'),
        ),
        # Обновляем существующие записи
        migrations.RunPython(set_new_building),
    ]