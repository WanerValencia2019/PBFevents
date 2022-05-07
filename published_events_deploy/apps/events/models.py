import uuid

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model
from django.utils.timezone import now
from slugify import slugify

from published_events_deploy.apps.events.managers import EventManager, TicketTypeManager
from published_events_deploy.apps.multimedia.models import Image

User = get_user_model()


class Category(models.Model):
    id = models.CharField(max_length=36, primary_key=True, blank=True)
    name = models.CharField(max_length=80, verbose_name="Nombre")
    description = models.CharField(max_length=100, verbose_name="Descripción(corta)")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categoría de evento"
        verbose_name_plural = "Categorías de eventos"


@receiver(pre_save, sender=Category)
def set_uuid(instance, *args, **kwargs):
    if not instance.id:
        instance.id = uuid.uuid4().hex
        print(instance.id)


class TicketType(models.Model):
    id = models.CharField(max_length=36, primary_key=True, blank=True)
    name = models.CharField(max_length=120, verbose_name="Nombre del tipo de entrada")
    description = models.CharField(max_length=150, verbose_name="Descripción corta")
    unit_price = models.FloatField(default=0.0, verbose_name="Precio del ticket")
    availables = models.IntegerField(default=0, verbose_name="Espacios disponibles para esta entrada")
    ticket_sales = models.IntegerField(default=0, verbose_name="Tickets vendidos", blank=True)
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, related_name="ticket_type_event")
    objects = TicketTypeManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_space_availables_on_event(self):
        self.event.space_available = self.event.space_available - self.availables
        self.event.save()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tipo de tiquete"
        verbose_name_plural = "Tipos de tiquetes"


@receiver(pre_save, sender=TicketType)
def set_uuid(instance, *args, **kwargs):
    if not instance.id:
        instance.id = uuid.uuid4().hex


@receiver(post_save, sender=TicketType)
def set_uuid(instance, *args, **kwargs):
    instance.update_space_availables_on_event()


class Event(models.Model):
    id = models.CharField(max_length=36, primary_key=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Creado por",
                                   related_name="user_events")
    title = models.CharField(max_length=150, verbose_name="Titulo del evento", null=False, blank=False)
    description = models.TextField(verbose_name="Descripción")
    slug = models.CharField(max_length=200, verbose_name="Slug", blank=True, null=False)
    space_available = models.IntegerField(default=1, verbose_name="Cantidad de cupos disponibles")
    image = models.OneToOneField(Image, verbose_name="Imagen principal", max_length=5000, null=True,
                                 on_delete=models.SET_NULL,
                                 related_name="image_events")
    other_images = models.ManyToManyField(Image, verbose_name="Otras imagenes",
                                          related_name="other_images_event", blank=True)
    address = models.CharField(verbose_name="Dirección", max_length=150, null=True)
    sell_limit_date = models.DateTimeField(default=now, verbose_name="Fecha limite de venta")
    start_date = models.DateTimeField(default=now, verbose_name="Fecha de inicio")
    latitude = models.CharField(max_length=100, null=False, blank=True, verbose_name="Latitud")
    longitude = models.CharField(max_length=100, null=False, blank=True, verbose_name="Longitud")
    end_date = models.DateTimeField(default=now, verbose_name="Fecha de finalización")
    categories = models.ManyToManyField(Category, related_name="categories_event")
    objects = EventManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"


@receiver(pre_save, sender=Event)
def set_uuid(instance, *args, **kwargs):
    if not instance.id:
        instance.id = uuid.uuid4().hex

    if not instance.slug:
        instance.slug = slugify(instance.title)


class Assistant(models.Model):
    id = models.CharField(max_length=36, primary_key=True, blank=True)
    full_name = models.CharField(max_length=150, verbose_name="Nombre completo")
    email = models.EmailField(verbose_name="Correo electronico")
    phone = models.CharField(max_length=12, verbose_name="Telefono")
    identification = models.CharField(max_length=12, verbose_name="Identificación")
    ticket = models.ForeignKey(TicketType,verbose_name="Ticker(Entrada)", on_delete=models.RESTRICT)
    ticket_quantity = models.IntegerField(default=1, verbose_name="Cantidad de tickets")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name



@receiver(pre_save, sender=Assistant)
def set_uuid(instance, *args, **kwargs):
    if not instance.id:
        instance.id = uuid.uuid4().hex
