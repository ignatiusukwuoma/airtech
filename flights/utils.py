from datetime import timedelta, datetime
from geopy import distance


def get_flight_duration(departure, destination):
    departure_coordinates = (departure.latitude, departure.longitude)
    destination_coordinates = (destination.latitude, destination.longitude)
    travel_distance = distance.distance(departure_coordinates, destination_coordinates).km
    avg_speed = 900
    time = travel_distance / avg_speed
    duration = timedelta(hours=time)
    return duration


def flight_date_range(day):
    start_date = day - timedelta(days=3)
    end_date = day + timedelta(days=3)
    date_range = (start_date, end_date)
    return date_range


def tomorrow():
    day = datetime.now().date() + timedelta(days=1)
    return day.strftime('%Y-%m-%d')


def generate_flight_dates(date_range, flights):
    start_date, end_date = date_range
    days = (end_date - start_date).days + 1
    date_list = [start_date + timedelta(days=x) for x in range(0, days)]
    flight_dates = []
    for day in date_list:
        flight_date = {'date': day}
        flights_on_day = []
        cheapest_flight = 0
        for flight in flights:
            if flight.last_update.date() == day:
                flights_on_day.append(flight)
                if flight.price_economy < cheapest_flight or cheapest_flight == 0:
                    cheapest_flight = flight.price_economy
        flight_date['flights'] = flights_on_day
        flight_date['cheapest_flight'] = cheapest_flight
        flight_dates.append(flight_date)
    return flight_dates


def add_time(date_time, time_delta):
    return date_time + time_delta
