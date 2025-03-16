from django.shortcuts import render


from property.models import Flat


def format_price(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def show_flats(request):
    town = request.GET.get('town')
    min_price = format_price(request.GET.get('min_price'))
    max_price = format_price(request.GET.get('max_price'))
    new_building = request.GET.get('new_building')

    flats = Flat.objects.all()
    if town:
        flats = flats.filter(town=town)
    if min_price:
        flats = flats.filter(price__gt=min_price)
    if max_price:
        flats = flats.filter(price__lt=max_price)
        # Фильтрация по новостройке
    if new_building == '1':  # строка '1' означает новостройку
        flats = flats.filter(new_building=True)
    elif new_building == '0':  # строка '0' означает старое здание
        flats = flats.filter(new_building=False)

    towns = Flat.objects.values_list(
        'town', flat=True).distinct().order_by('town')
    return render(request, 'flats_list.html', {
        'flats': flats[:10],
        'towns': towns,
        'active_town': town,
        'max_price': max_price,
        'min_price': min_price,
        'new_building': new_building})
