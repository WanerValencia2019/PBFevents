from django.contrib import admin
from published_events_deploy.apps.events.forms import TicketTypeForm
from published_events_deploy.apps.events.models import TicketType, Event, Category, Assistant


class TicketTypeAdmin(admin.ModelAdmin):
    form = TicketTypeForm
    list_display = ["name", "description", "unit_price", "availables", "event"]
    readonly_fields = ("ticket_sales",)


class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "space_available", "start_date", "end_date"]


class AssistantAdmin(admin.ModelAdmin):
    list_display = ["full_name", "email", "ticket", "ticket_quantity"]


admin.site.register(TicketType, TicketTypeAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Category)
admin.site.register(Assistant, AssistantAdmin)
