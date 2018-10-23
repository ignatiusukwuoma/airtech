from django.db.models import Model, CharField, DateTimeField, DecimalField, IntegerField, DurationField, ForeignKey, SET_NULL
from .utils import get_flight_duration


class Location(Model):
    """A class to define the various travel locations"""

    iata = CharField(max_length=3)
    airport = CharField(max_length=100)
    city = CharField(max_length=50)
    country = CharField(max_length=50)
    latitude = DecimalField(max_digits=9, decimal_places=6)
    longitude = DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"{self.city}, {self.country}"


class Aircraft(Model):
    """A class defining available Air crafts"""

    manufacturer = CharField(max_length=50)
    model = CharField(max_length=50)
    capacity = IntegerField(default=500)

    def __str__(self):
        return f"{self.manufacturer} {self.model}"


class FlightStatus(Model):
    """A class defining the status of a Flight"""

    name = CharField(max_length=50)

    def __str__(self):
        return self.name


class Flight(Model):
    """A typical class defining a flight"""

    # Fields
    flight_number = CharField(max_length=20, unique=True, help_text='Enter flight number')
    departure = ForeignKey(Location, on_delete=SET_NULL, null=True)
    destination = ForeignKey(Location, on_delete=SET_NULL, null=True, related_name='destination_set')
    flight_duration = DurationField(blank=True)
    scheduled = DateTimeField()
    last_update = DateTimeField(blank=True)
    flight_status = ForeignKey(FlightStatus, on_delete=SET_NULL, null=True, default=1)
    aircraft = ForeignKey(Aircraft, on_delete=SET_NULL, null=True)
    price_economy = DecimalField(max_digits=9, decimal_places=2)
    price_business = DecimalField(max_digits=9, decimal_places=2)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.flight_duration:
            duration = get_flight_duration(self.departure, self.destination)
            self.flight_duration = duration
        if not self.last_update:
            self.last_update = self.scheduled

        super().save(*args, **kwargs)

    def __str__(self):
        """String for representing the Flight object (in Admin site etc.)."""
        return f"{self.flight_number}, {self.departure.city} - {self.destination.city}"
