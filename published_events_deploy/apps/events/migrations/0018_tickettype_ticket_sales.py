# Generated by Django 3.2.12 on 2022-04-19 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0017_alter_event_other_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickettype',
            name='ticket_sales',
            field=models.IntegerField(default=0, editable=False, verbose_name='Tickets vendidos'),
        ),
    ]