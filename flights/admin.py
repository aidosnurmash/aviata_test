from django.contrib import admin

# Register your models here.
from flights.models import Flight, City


class FlightAdmin(admin.ModelAdmin):
    pass


class CityAdmin(admin.ModelAdmin):
    pass


admin.site.register(Flight, FlightAdmin)
admin.site.register(City, CityAdmin)
