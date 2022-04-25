from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Manager


class EventManager(Manager):
    def get_queryset(self):
        return super(EventManager, self).get_queryset()

    def get_assistants(self, event_id) -> list or None:
        try:
            self.get_queryset().get(id=event_id)
            assistants = []
            return assistants
        except ObjectDoesNotExist as ex:
            return None
