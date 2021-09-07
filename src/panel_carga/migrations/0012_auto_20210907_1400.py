# Generated by Django 3.1.1 on 2021-09-07 17:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('panel_carga', '0011_auto_20210823_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='encargado',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='Encargado'),
        ),
    ]
