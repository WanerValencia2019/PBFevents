# Generated by Django 3.2.12 on 2022-02-18 00:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=150, verbose_name='Titulo del evento')),
                ('description', models.TextField(verbose_name='Descripción')),
                ('slug', models.CharField(blank=True, max_length=200, verbose_name='Slug')),
                ('space_available', models.IntegerField(default=1, verbose_name='Cantidad de cupos disponibles')),
            ],
        ),
        migrations.CreateModel(
            name='TicketType',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=120, verbose_name='Nombre del tipo de entrada')),
                ('description', models.CharField(max_length=150, verbose_name='Descripción corta')),
                ('unit_price', models.FloatField(default=0.0, verbose_name='Precio del ticket')),
                ('availables', models.IntegerField(default=1, verbose_name='Espacios disponibles para esta entrada')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_type_event', to='events.event')),
            ],
        ),
    ]
