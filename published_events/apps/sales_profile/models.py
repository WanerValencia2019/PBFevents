import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver

User = get_user_model()


#
class Withdrawal(models.Model):
    id = models.CharField(max_length=36, primary_key=True, blank=True)
    sale_profile = models.ForeignKey("SaleProfile", verbose_name="Perfil de usuario", on_delete=models.RESTRICT,
                                     related_name="withdraw_sale_profile")
    amount_withdrawn = models.FloatField(verbose_name="Dinero a retirado")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(self.sale_profile.user.username, self.amount_withdrawn)


@receiver(pre_save, sender=Withdrawal)
def set_uuid(instance, *args, **kwargs):
    if not instance.id:
        instance.id = uuid.uuid4().hex


class SaleProfile(models.Model):
    id = models.CharField(max_length=36, primary_key=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario",
                                related_name="user_sale_profile")
    amount_available = models.FloatField(verbose_name="Dinero disponible", default=0.0)
    amount_retired = models.FloatField(verbose_name="Dinero retirado", default=0.0)
    last_withdraw = models.DateTimeField(verbose_name="Fecha de ultimo retiro")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


@receiver(pre_save, sender=SaleProfile)
def set_uuid(instance, *args, **kwargs):
    if not instance.id:
        instance.id = uuid.uuid4().hex
