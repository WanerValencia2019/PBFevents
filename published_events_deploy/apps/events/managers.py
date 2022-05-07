from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Manager


class EventManager(Manager):
    def get_queryset(self):
        return super(EventManager, self).get_queryset()

    def get_assistants(self, event_id) -> list or None:
        try:
            self.get_queryset().filter(id=event_id)
            assistants = []
            return assistants
        except ObjectDoesNotExist as ex:
            return None

class TicketTypeManager(Manager):
    def get_queryset(self):
        return super(TicketTypeManager, self).get_queryset()

    def get_ticket_types(self, event_id) -> list or None:
        try:
            self.get_queryset().filter(event__id=event_id)
            ticket_types = []
            return ticket_types
        except ObjectDoesNotExist as ex:
            return None