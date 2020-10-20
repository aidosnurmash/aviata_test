import random
from time import sleep
import datetime

import requests
from celery.schedules import crontab
from django.core.cache import cache

from flights.models import Flight, City
from aviata_test.celery import app


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls hello_world every 10 seconds.
    # sender.add_periodic_task(10.0, hello_world.s(), name='print every 10')

    sender.add_periodic_task(crontab(hour=0, minute=0), update_all_flights.s(), name='update all flights')


@app.task
def hello_world():
    sleep(2)  # поставим тут задержку в 10 сек для демонстрации ассинхрности
    print('Hello World')


def valid_booking(token):
    CHECK_URL = 'https://booking-api.skypicker.com/api/v0.1/check_flights?'
    params = {
        'v': 2,
        'booking_token': token,
        'bnum': 1,
        'pnum': 1,
        'currency': 'KZT',
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36' + str(
            random.randint(0, 100)),
        'Content-Type': 'application/json; charset=utf-8',
    }
    data = None
    for _ in range(10):
        try:
            resp = requests.get(url=CHECK_URL, headers=headers, params=params)
            data = resp.json()
            break
        except Exception as e:
            print('valid_booking', resp.headers, e)

    return data['flights_checked'] if type(data) == dict else False


def update_flight_next_x_days(flight_id, fly_from, fly_to, num_of_days):
    cur_date = datetime.datetime.today()
    dates = []
    for day in range(num_of_days):
        dates.append(cur_date)
        cur_date = cur_date + datetime.timedelta(days=1)

    for date in dates:
        cur_date = date.strftime("%d/%m/%Y")
        flights = get_flights(fly_from, fly_to, cur_date, cur_date)
        if flights:
            cache.set('flight_id{0}_{1}'.format(flight_id, cur_date), flights)
            # print('flights', flights)
            print(cache.get('flight_id{0}_{1}'.format(flight_id, cur_date)))


def get_flights(fly_from, fly_to, str_date, end_date):
    DATA_URL = 'https://api.skypicker.com/flights?'

    params = {
        'fly_from': fly_from,
        'fly_to': fly_to,
        'partner': 'picky',
        'date_from': str_date,
        'date_to': end_date,
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36' + str(
            random.randint(0, 100)),
        'Content-Type': 'application/json; charset=utf-8',
    }
    try:
        resp = requests.get(url=DATA_URL, headers=headers, params=params)
        data = resp.json()
    except Exception as e:
        print('get_flights', resp.headers, e)
        return None

    all_flights = []
    cur = data.get('data', [])
    if not cur:
        print('data=', data)
    for choice in cur:
        flight = dict()
        flight['booking_token'] = choice['booking_token']
        flight['price'] = choice['price']
        flight['time'] = datetime.datetime.fromtimestamp(choice['dTimeUTC'])
        flight['airline'] = ', '.join(choice['airlines']),
        flight['duration'] = choice['fly_duration'],
        flight['seats'] = 0
        all_flights.append(flight)

    return all_flights


LIST_OF_CITIES = [('ALA', 'Almaty'), ('NQZ', 'Nur-Sultan'), ('MOW', 'Moscow'), ('KZO', 'Kyzylorda')]


@app.task
def init_all_flights():
    Flight.objects.all().delete()
    City.objects.all().delete()
    cache.clear()
    for x, y in LIST_OF_CITIES:
        City.objects.create(city_code=x, city_name=y).save()

    for x, y in LIST_OF_CITIES:
        for a, b in LIST_OF_CITIES:
            if x == a:
                continue
            city_from = City.objects.filter(city_code=x).first()
            city_to = City.objects.filter(city_code=a).first()
            Flight.objects.create(city_from=city_from, city_to=city_to).save()

    update_all_flights()


@app.task
def update_all_flights():
    print('update flights')
    flights = Flight.objects.all()
    for flight in flights:
        print(flight)
        update_flight_next_x_days(flight.id, flight.city_from.city_code, flight.city_to.city_code, 3)
