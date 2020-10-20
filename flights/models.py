from django.db import models


# Create your models here.


class City(models.Model):
    city_name = models.CharField(max_length=100)
    city_code = models.CharField(max_length=10)

    def get_short_name(self):
        return self.city_code

    def get_full_name(self):
        return self.city_name + "(" + self.city_code + ")"

    def __str__(self):
        return self.city_name + "(" + self.city_code + ")"


class Flight(models.Model):
    city_from = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city_from')
    city_to = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city_to')

    def get_full_name(self):
        return self.city_from.get_full_name() + '-' + self.city_to.get_full_name()

    def get_short_name(self):
        return self.city_from.get_short_name() + '-' + self.city_to.get_short_name()

    def __str__(self):
        return self.get_full_name()
