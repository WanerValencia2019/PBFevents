from published_events_deploy.apps.transactions.models import Transaction, TransactionStatus
from published_events_deploy.apps.sales_profile.models import SaleProfile
from published_events_deploy.apps.events.models import TicketType, Assistant
from django.core.exceptions import ObjectDoesNotExist

"""
payment_result -> {
    status,
    amount
}
"""

def create_transaction(user_identification:str, ticket_type:TicketType, ticket_amount:int, payment_result:dict) -> Transaction:
    transaction = Transaction()
    transaction.user_identification = user_identification
    transaction.ticket_type = ticket_type
    transaction.ticket_amount = ticket_amount


    if payment_result.get('status') == "CREATED":
        transaction.status = TransactionStatus.CREATED

    elif payment_result.get('status') == "PAYED":
        transaction.status = TransactionStatus.PAYED
        user = ticket_type.event.created_by
        ticket_type.ticket_sales += ticket_amount
        ticket_type.save()

        assistant = Assistant()
        assistant.full_name = payment_result.get("buyer_full_name")
        assistant.email = payment_result.get("email")
        assistant.phone = payment_result.get("phone")
        assistant.identification = payment_result.get("identification")
        assistant.ticket = ticket_type
        assistant.ticket_quantity = ticket_amount

        assistant.save()


        try:
            sale_profile = SaleProfile.objects.get(user=user)
            sale_profile.amount_available += float(payment_result.get('amount'))
            sale_profile.save()
        except ObjectDoesNotExist as ex:
            sale_profile = SaleProfile()
            sale_profile.user = user
            sale_profile.amount_available += float(payment_result.get('amount'))
            sale_profile.save()
    else:
        transaction.status = TransactionStatus.CANCELED

    transaction.save()

    return transaction
