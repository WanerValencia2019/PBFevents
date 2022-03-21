from django.forms import ModelForm, ValidationError

from published_events_deploy.apps.events.models import TicketType, Event


class TicketTypeForm(ModelForm):
    class Meta:
        model = TicketType
        fields = ['name', "description", 'unit_price', 'availables', 'event']

    def clean_availables(self):
        event_id = self.data.get('event')
        event = Event.objects.get(id=event_id)
        availables = self.cleaned_data.get('availables')

        if availables > event.space_available:
            raise ValidationError(
                'La cantidad supera los tickets disponibles en el evento ({})'.format(event.space_available))
        return availables
