from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Flat, Complaint, Owner


class OwnerInline(admin.TabularInline):
    model = Flat.owners.through
    raw_id_fields = ['owner', 'flat']

class FlatAdmin(admin.ModelAdmin):
    search_fields = ['town', 'town_district', 'address']
    readonly_fields = ['created_at']

    list_display = ['address', 'price', 'new_building', 'construction_year', 'town', 'get_owners']
    list_editable = ['new_building']

    list_filter = ['new_building', 'rooms_number', 'has_balcony', 'active']
    inlines = [OwnerInline]
    raw_id_fields = ['likes']

    def get_owners(self, obj):
        owners = obj.owner_apartaments.all()  # Получаем всех владельцев
        if owners:
            return format_html(", ".join([
                f'<a href="{reverse("admin:property_owner_change", args=[owner.id])}">{owner.owner}</a>'
                for owner in owners
            ]))  # Создаем ссылки на владельцев
        return "Нет владельцев"

    get_owners.short_description = "Собственники"


class ComplaintsAdmin(admin.ModelAdmin):
    raw_id_fields = ['apartment']


class OwnerAdmin(admin.ModelAdmin):
    raw_id_fields = ['apartaments']
    list_display = ['owner', 'owner_correct_phone', 'get_apartaments']  # Добавляем колонку "Квартиры"

    def get_apartaments(self, obj):
        flats = obj.apartaments.all()  # Получаем все квартиры владельца
        if flats:
            return format_html(", ".join([
                f'<a href="{reverse("admin:property_flat_change", args=[flat.id])}">{flat.address}</a>'
                for flat in flats
            ]))  # Создаем ссылки на квартиры
        return "Нет квартир"

    get_apartaments.short_description = "Квартиры"


admin.site.register(Flat, FlatAdmin)
admin.site.register(Complaint, ComplaintsAdmin)
admin.site.register(Owner, OwnerAdmin)
