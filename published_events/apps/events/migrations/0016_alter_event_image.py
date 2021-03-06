# Generated by Django 3.2.12 on 2022-03-14 17:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('multimedia', '0002_alter_image_image'),
        ('events', '0015_auto_20220314_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.OneToOneField(max_length=5000, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='image_events', to='multimedia.image', verbose_name='Imagen principal'),
        ),
    ]
