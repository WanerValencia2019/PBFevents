# Generated by Django 3.2.12 on 2022-02-18 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20220217_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.CharField(blank=True, max_length=36, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='id',
            field=models.CharField(blank=True, max_length=36, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='tickettype',
            name='availables',
            field=models.IntegerField(default=0, verbose_name='Espacios disponibles para esta entrada'),
        ),
        migrations.AlterField(
            model_name='tickettype',
            name='id',
            field=models.CharField(blank=True, max_length=36, primary_key=True, serialize=False),
        ),
    ]