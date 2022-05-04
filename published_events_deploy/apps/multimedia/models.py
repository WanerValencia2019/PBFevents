import uuid

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Image(models.Model):
    id = models.CharField(max_length=36, primary_key=True, blank=True)
    image = models.ImageField(verbose_name="Imagen",upload_to="images/", max_length=2000, null=False)

    def __str__(self):
        return self.image.name


@receiver(pre_save, sender=Image)
def set_uuid(instance, *args, **kwargs):
    if not instance.id:
        instance.id = uuid.uuid4().hex
