from django.urls import path
from .views import flights, flight_status, signup, review_flight, select_flight

app_name = 'flights'
urlpatterns = [
    path('', flights, name='search_flights'),
    path('flight-status/', flight_status, name='flight_status'),
    path('select/', select_flight, name='select_flight'),
    path('review/', review_flight, name='review_flight'),
    path('signup/', signup, name='signup')
]
