import datetime

from django.http import HttpResponse
from django.shortcuts import render

from aviata_test.tasks import update_all_flights, hello_world, init_all_flights
from flights.commands import get_flights_from_cache
from flights.forms import FlightForm
from flights.models import Flight


def index(request):
    flights = []

    flight_date = datetime.date.today()
    if request.method == 'POST':
        form = FlightForm(request.POST)
        if form.is_valid():
            flight_date = datetime.datetime.strptime(form.data['date'], '%Y-%m-%d')
            flight_id = int(form.data['flights'])
            cur_flight = Flight.objects.all().get(pk=flight_id)
            flights = get_flights_from_cache(flight_id, flight_date)
            return render(request, 'index.html',
                          context={'form': form, 'flights': flights, 'flight_date': flight_date,
                                   'flight_name': cur_flight.get_full_name()})
    # print(flight_date)
    return render(request, 'index.html',
                  context={'form': FlightForm(), 'flights': flights, 'flight_name': '', 'flight_date': flight_date})


def update_cache(request):
    print('OK')
    update_all_flights.delay()
    return HttpResponse("update all flights")


def init_flights(request):
    print('OK')
    init_all_flights.delay()
    return HttpResponse('init all flights start')


def all_flights(request):
    dates = []
    num_of_days = 30
    cur_date = datetime.datetime.today()
    flights = []

    for day in range(num_of_days):
        dates.append(cur_date)
        cur_date = cur_date + datetime.timedelta(days=1)
    for day in dates:
        for flight in Flight.objects.all():
            cur = get_flights_from_cache(flight.id, day)
            if cur:
                flights.extend(cur)

    return render(request, 'flight.html',
                  context={'flights': flights})
