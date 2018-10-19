from django.contrib import admin

from .models import Ticket, BookingStatus, Trip

admin.site.register(Ticket)
admin.site.register(BookingStatus)
admin.site.register(Trip)
