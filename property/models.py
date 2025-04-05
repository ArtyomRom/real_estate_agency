from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField



class Flat(models.Model):
    # owner = models.CharField('ФИО владельца', max_length=200)
    # owner_pure_phone = PhoneNumberField(region="RU", verbose_name="Нормализованный номер владельца", blank=True,
    #                                     null=True)
    owners = models.ManyToManyField('Owner', through='FlatOwnership', related_name='owned_flats')
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
    likes = models.ManyToManyField(User, verbose_name='Кто лайкнул', blank=True, related_name='liked_flats')

    def save(self, *args, **kwargs):
        """Автоматически определяет, новостройка или старое здание"""
        if self.construction_year >= 2015:
            self.new_building = True
        else:
            self.new_building = False
        super().save(*args, **kwargs)

    def get_owners(self):
        return ", ".join([str(owner.owner) for owner in self.owners_list.all()])

    get_owners.short_description = "Собственники"

    def __str__(self):
        return f'{self.town}, {self.address} ({self.price}р.)'


class Owner(models.Model):
    """Собственники квартир"""
    owner = models.CharField(verbose_name="ФИО владельца", max_length=200)
    owner_correct_phone = PhoneNumberField(region="RU", verbose_name="Нормализованный номер владельца",  default='+79999999999')
    apartaments = models.ManyToManyField("Flat", through="FlatOwnership", related_name="owners_list")

    def __str__(self):
        return f'{self.owner} - {self.owner_correct_phone}'

class FlatOwnership(models.Model):
    """Связь между квартирами и владельцами"""
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name="ownerships")
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE, related_name="ownership_owners")

    class Meta:
        unique_together = ('owner', 'flat')  # Запрещаем дублирование связей

    def __str__(self):
        return f'{self.owner} владеет {self.flat.address}'


class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Кто жаловался',
                             related_name='complaints')
    apartment = models.ForeignKey(Flat, on_delete=models.CASCADE, verbose_name='Квартира, на которую жаловались',
                                  related_name='complaints')
    complaint = models.TextField(verbose_name='Текст жалобы')
