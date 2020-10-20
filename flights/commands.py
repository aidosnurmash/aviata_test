import datetime

from django.core.cache import cache


def get_flights_from_cache(flight_id, flight_date):
    flights = []
    api_date_format = '%d-%m-%YT%H:%M'
    cur_date = flight_date.strftime("%d/%m/%Y")
    flights_cache = cache.get('flight_id{0}_{1}'.format(flight_id, cur_date))
    #print(flights_cache)

    return flights_cache