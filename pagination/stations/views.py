from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
import csv

with open(settings.BUS_STATION_CSV, newline='', encoding="utf-8") as f:
    csv_data = csv.DictReader(f)
    bus_stations_list = []
    for row in csv_data:
        bus_stations_list.append(row)


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    current_page = int(request.GET.get('page', 1))
    paginator = Paginator(bus_stations_list, 10)
    page = paginator.get_page(current_page)
    context = {
        'bus_stations': page.object_list,
        'page': page
    }
    return render(request, 'stations/index.html', context)

