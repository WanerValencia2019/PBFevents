# Generated by Django 3.2.12 on 2022-04-09 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_customuser_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='users/%Y/%m/%d', verbose_name='Imagen de perfil'),
        ),
    ]