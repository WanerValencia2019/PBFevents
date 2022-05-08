from enum import Enum
import uuid
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from published_events_deploy.apps.events.models import TicketType

class TransactionStatus(Enum):
    CREATED='CREATED'
    PAYED='PAYED'
    CANCELED='CANCELED'

choices = [(tag, tag.value) for tag in TransactionStatus]

class Transaction(models.Model):
    id = models.CharField(max_length=36, primary_key=True, blank=True)
    user_identification = models.CharField(max_length=12)
    ticket_type = models.ForeignKey(TicketType,verbose_name="Ticket de la transacción", on_delete=models.RESTRICT)
    ticket_amount = models.IntegerField(default=1)
    total_price = models.FloatField(default=0.0)
    status = models.CharField(max_length=50,choices=choices,default=TransactionStatus.CREATED)
    meta_data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

@receiver(pre_save, sender=Transaction)
def set_uuid(instance, *args, **kwargs):
    if not instance.id:
        instance.id = uuid.uuid4().hex