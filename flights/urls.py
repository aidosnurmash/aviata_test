from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('update', views.update_cache, name='update_cache'),
    path('init', views.init_flights, name='init'),
    path('all_flights', views.all_flights, name='flights_from_cache'),

]