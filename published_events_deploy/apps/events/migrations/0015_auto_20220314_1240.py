# Generated by Django 3.2.12 on 2022-03-14 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multimedia', '0002_alter_image_image'),
        ('events', '0014_alter_event_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='other_images',
        ),
        migrations.AddField(
            model_name='event',
            name='other_images',
            field=models.ManyToManyField(related_name='other_images_event', to='multimedia.Image', verbose_name='Otras imagenes'),
        ),
    ]