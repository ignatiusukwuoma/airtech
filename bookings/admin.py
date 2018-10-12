from django.contrib import admin

from .models import Ticket, TicketStatus, Trip

admin.site.register(Ticket)
admin.site.register(TicketStatus)
admin.site.register(Trip)
