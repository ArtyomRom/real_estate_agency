from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class Flat(models.Model):
    owner = models.CharField('ФИО владельца', max_length=200)
    owner_pure_phone = PhoneNumberField(region="RU", verbose_name="Нормализованный номер владельца", blank=True,
                                        null=True)
    created_at = models.DateTimeField(
        'Когда создано объявление',
        default=timezone.now,
        db_index=True)

    description = models.TextField('Текст объявления', blank=True)
    price = models.IntegerField('Цена квартиры', db_index=True)

    town = models.CharField(
        'Город, где находится квартира',
        max_length=50,
        db_index=True)
    town_district = models.CharField(
        'Район города, где находится квартира',
        max_length=50,
        blank=True,
        help_text='Чертаново Южное')
    address = models.TextField(
        'Адрес квартиры',
        help_text='ул. Подольских курсантов д.5 кв.4')
    floor = models.CharField(
        'Этаж',
        max_length=3,
        help_text='Первый этаж, последний этаж, пятый этаж')

    rooms_number = models.IntegerField(
        'Количество комнат в квартире',
        db_index=True)
    living_area = models.IntegerField(
        'количество жилых кв.метров',
        null=True,
        blank=True,
        db_index=True)

    # has_balcony = models.NullBooleanField('Наличие балкона', db_index=True)
    has_balcony = models.BooleanField('Наличие балкона', null=True, blank=True, db_index=True)
    active = models.BooleanField('Активно-ли объявление', db_index=True)
    construction_year = models.IntegerField(
        'Год постройки здания',
        null=True,
        blank=True,
        db_index=True)
    new_building = models.BooleanField('Новостройка',
                                       choices=[(True, "Да"),
                                                (False, "Нет")],
                                       default=False,  # Устанавливаем значение по умолчанию
                                       null=False,  # Убираем возможность быть NULL
                                       blank=True,
                                       db_index=True)
    likes = models.ManyToManyField(User, verbose_name='Кто лайкнул', blank=True)

    def save(self, *args, **kwargs):
        """Автоматически определяет, новостройка или старое здание"""
        if self.construction_year >= 2015:
            self.new_building = True
        else:
            self.new_building = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.town}, {self.address} ({self.price}р.)'


class Owner(models.Model):
    """Собственники квартир"""
    owner = models.CharField(verbose_name='ФИО владельца', max_length=200)
    owner_correct_phone = PhoneNumberField(region="RU", verbose_name="Нормализованный номер владельца", blank=True,
                                           null=True)
    apartaments = models.ManyToManyField(Flat, related_name="owners",
                                         verbose_name='Квартиры в собственности')

    def __str__(self):
        return self.owner


class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Кто жаловался',
                             related_name='complaints')
    apartment = models.ForeignKey(Flat, on_delete=models.CASCADE, verbose_name='Квартира, на которую жаловались',
                                  related_name='complaints')
    complaint = models.TextField(verbose_name='Текст жалобы')
