from datetime import timedelta
from geopy import distance


def get_flight_duration(departure, destination):
    departure_coordinates = (departure.latitude, departure.longitude)
    destination_coordinates = (destination.latitude, destination.longitude)
    travel_distance = distance.distance(departure_coordinates, destination_coordinates).km
    avg_speed = 900
    time = travel_distance / avg_speed
    duration = timedelta(hours=time)
    return duration
