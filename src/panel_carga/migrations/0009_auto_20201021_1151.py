# Generated by Django 3.1.1 on 2020-10-21 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('panel_carga', '0008_paquete_documento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paquetedocumento',
            name='documento_id',
        ),
        migrations.RemoveField(
            model_name='paquetedocumento',
            name='paquete_id',
        ),
        migrations.DeleteModel(
            name='Paquete',
        ),
        migrations.DeleteModel(
            name='PaqueteDocumento',
        ),
    ]
