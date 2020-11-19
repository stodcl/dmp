# Generated by Django 3.1.1 on 2020-11-19 20:03

import bandeja_es.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bandeja_es', '0002_auto_20201116_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='version',
            name='paquete_fk',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bandeja_es.paquete', verbose_name=bandeja_es.models.Paquete),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='version',
            name='valido',
            field=models.BooleanField(default=1, verbose_name='Valido'),
        ),
    ]
