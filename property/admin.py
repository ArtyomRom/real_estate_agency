from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Flat, Complaint, Owner, FlatOwnership

class OwnerFlatshipInline(admin.TabularInline):
    model = FlatOwnership
    extra = 1
    raw_id_fields = ['owner']


class FlatAdmin(admin.ModelAdmin):
    search_fields = ['town', 'town_district', 'address']
    readonly_fields = ['created_at']
    list_display = ['address', 'price', 'new_building', 'construction_year', 'town', 'get_owners', 'new_building']
    list_editable = ['new_building']
    list_filter = ['new_building', 'rooms_number', 'has_balcony', 'active']
    raw_id_fields = ['likes']
    inlines = [OwnerFlatshipInline]

    def get_owners(self, obj):
        """Получаем всех владельцев квартиры через промежуточную таблицу"""
        owners = Owner.objects.filter(ownerships__flat=obj)  # Доступ через FlatOwnership

        if owners:
            return format_html(", ".join([
                f'<a href="{reverse("admin:property_owner_change", args=[owner.id])}">{owner}</a>'
                for owner in owners
            ]))  # Создаем ссылки на владельцев

        return "Нет владельцев"

    get_owners.short_description = "Собственники"


class ComplaintsAdmin(admin.ModelAdmin):
    raw_id_fields = ['apartment']

class FlatOwnershipInline(admin.TabularInline):
    model = FlatOwnership
    extra = 1
    raw_id_fields = ['flat']

class OwnerAdmin(admin.ModelAdmin):
    search_fields = ['owner', 'owner_correct_phone']
    list_display = ['owner', 'owner_correct_phone', 'get_apartaments']
    readonly_fields = ['get_apartaments']
    raw_id_fields = ['apartaments']  # Используем поиск по ID вместо медленного списка
    inlines = [FlatOwnershipInline]
    # raw_id_fields = ['flat']

    def get_apartaments(self, obj):
        """Отображает квартиры, принадлежащие владельцу"""
        flats = obj.ownerships.select_related('flat').values_list('flat__id', 'flat__address')

        if flats:
            return format_html(", ".join([
                f'<a href="{reverse("admin:property_flat_change", args=[flat_id])}">{flat_address}</a>'
                for flat_id, flat_address in flats
            ]))

        return "Нет квартир"

    get_apartaments.short_description = "Квартиры"



admin.site.register(Flat, FlatAdmin)
admin.site.register(Complaint, ComplaintsAdmin)
admin.site.register(Owner, OwnerAdmin)
