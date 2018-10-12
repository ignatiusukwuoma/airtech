from django.db.models import Model, CharField, DateTimeField, DecimalField, DurationField, ForeignKey, SET_NULL


class Location(Model):
    """A class to define the various travel locations"""

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
    flight_duration = DurationField()
    scheduled = DateTimeField()
    last_update = DateTimeField()
    flight_status = ForeignKey(FlightStatus, on_delete=SET_NULL, null=True)
    aircraft = ForeignKey(Aircraft, on_delete=SET_NULL, null=True)
    price_economy = DecimalField(max_digits=9, decimal_places=2)
    price_business = DecimalField(max_digits=9, decimal_places=2)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        """String for representing the Flight object (in Admin site etc.)."""
        return self.flight_number


