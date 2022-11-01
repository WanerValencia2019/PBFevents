from multiprocessing import Event
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from published_events_deploy.apps.events.models import Assistant, TicketType

from published_events_deploy.apps.transactions.models import Transaction


def send_ticket_mail(event: Event, assistant: Assistant, transaction: Transaction):
    """
    Send a mail to the user who bought a ticket.
    """
    print("CARGANDO ENVIO DEL MAIL")
    context = {
        "ticket_name": transaction.ticket_type.name,
        "security_code": assistant.security_code,
        "full_name": assistant.full_name,
        "email": assistant.email,
        "identification": assistant.identification,
        "phone": assistant.phone,
        "ticket_description": transaction.ticket_type.description,
        "ticket_price": transaction.ticket_type.unit_price,
        "ticket_quantity": transaction.ticket_amount,
        "total_price": transaction.total_price,
        "start_date": event.start_date,
        "end_date": event.end_date,
    }

    print("CONTEXT ", context)
    try:
        template = get_template('mails/send_ticket.html')
        html_content = template.render(context)

        msg = EmailMultiAlternatives(
            # title:
            "Entrada a el evento {}".format(event.title),
            # message:
            html_content,
            # from:
            "hit.mindblog@gmail.com",
            # to:
            ["valenciawaner@gmail.com", assistant.email],
            ["valenciawaner@gmail.com", "elkin10cuesta@gmail.com"]
        )
        msg.content_subtype = "html"
        msg.send()
    except Exception as e:
        print("ERROR BLANCO ", e)
