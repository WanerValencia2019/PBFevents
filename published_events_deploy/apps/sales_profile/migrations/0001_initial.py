# Generated by Django 3.2.12 on 2022-03-14 19:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SaleProfile',
            fields=[
                ('id', models.CharField(blank=True, max_length=36, primary_key=True, serialize=False)),
                ('amount_available', models.FloatField(default=0.0, verbose_name='Dinero disponible')),
                ('amount_retired', models.FloatField(default=0.0, verbose_name='Dinero retirado')),
                ('last_withdraw', models.DateTimeField(verbose_name='Fecha de ultimo retiro')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_sale_profile', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
        ),
    ]