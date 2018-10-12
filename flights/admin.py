from django.contrib import admin

# Register your models here.
from .models import Location, Aircraft, FlightStatus, Flight

admin.site.register(Location)
admin.site.register(Aircraft)
admin.site.register(FlightStatus)
admin.site.register(Flight)
