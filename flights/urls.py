from django.urls import path
from .views import flights, flight_status

app_name = 'flights'
urlpatterns = [
    path('', flights, name='search_flights'),
    path('flight-status/', flight_status, name='flight_status')
]
