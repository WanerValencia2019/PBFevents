from django.contrib import admin

from published_events.apps.events.forms import TicketTypeForm
from published_events.apps.events.models import TicketType, Event, Category


class TicketTypeAdmin(admin.ModelAdmin):
    form = TicketTypeForm
    list_display = ["name", "description", "unit_price", "availables", "event"]


class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "space_available", "start_date", "end_date"]


admin.site.register(TicketType, TicketTypeAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Category)
