import threading
from uuid import uuid4
from published_events_deploy.apps.transactions.models import Transaction, TransactionStatus
from published_events_deploy.apps.sales_profile.models import SaleProfile
from published_events_deploy.apps.events.models import TicketType, Assistant
from django.core.exceptions import ObjectDoesNotExist

from django.db import transaction

from published_events_deploy.utils.mails import send_ticket_mail

"""
payment_result -> {
    status,
    amount
}
"""

def create_transaction(user_identification:str, ticket_type:TicketType, ticket_amount:int, payment_result:dict) -> Transaction:
    transaction = Transaction()
    transaction.id = payment_result.get("reference_code", uuid4().hex)
    transaction.user_identification = user_identification
    transaction.ticket_type = ticket_type
    transaction.ticket_amount = ticket_amount
    
    transaction.total_price = ticket_type.unit_price * ticket_amount

    meta_data = {
            "email" : payment_result.get("email", None),
            "buyer_full_name": payment_result.get("buyer_full_name", None),
            "phone" : payment_result.get("phone", None),
            "ticket_quantity": payment_result.get("quantity", None),
            "total_price": transaction.total_price,
            "amount": payment_result.get("amount", None),
            "identification":  payment_result.get("identification", None),
    }

    transaction.meta_data = meta_data

    transaction.status = TransactionStatus.CREATED
    transaction.save()

    return transaction

@transaction.atomic
def pay_transaction(transaction:Transaction) -> any:
    transaction.status = TransactionStatus.PAYED
    transaction.save()

    ticket_type = transaction.ticket_type
    user = ticket_type.event.created_by
    ticket_type.ticket_sales += transaction.ticket_amount
    ticket_type.save()

    assistant = Assistant()
    assistant.full_name = transaction.meta_data.get("buyer_full_name", None)
    assistant.email = transaction.meta_data.get("email", None)
    assistant.phone = transaction.meta_data.get("phone", None)
    assistant.identification = transaction.meta_data.get("identification", None)
    assistant.ticket = ticket_type
    assistant.security_code = str(transaction.meta_data.get("identification", "")).upper() + "-" + str(uuid4().hex)[0:8].upper()
    assistant.ticket_quantity = transaction.ticket_amount

    assistant.save()
    print("assistant saved")
    print(assistant)
    print("assistant saved")
    try:
        sale_profile = SaleProfile.objects.get(user=user)
        sale_profile.amount_available += float(transaction.total_price)
        sale_profile.save()
    except ObjectDoesNotExist as ex:
        sale_profile = SaleProfile()
        sale_profile.user = user
        sale_profile.amount_available += float(transaction.total_price)
        sale_profile.save()

    return transaction, assistant

def cancel_transaction(transaction:Transaction) -> Transaction:
    transaction.status = TransactionStatus.CANCELED
    transaction.save()
