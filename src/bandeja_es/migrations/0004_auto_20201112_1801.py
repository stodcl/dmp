# Generated by Django 3.1.1 on 2020-11-12 18:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bandeja_es', '0003_auto_20201110_1615'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='version',
            name='is_cliente_contratista',
        ),
        migrations.AlterField(
            model_name='borrador',
            name='nombre',
            field=models.CharField(max_length=100, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='version',
            name='estado_cliente',
            field=models.IntegerField(blank=True, choices=[(1, 'Aprobado con Comentarios'), (2, 'Rechazado'), (3, 'Eliminado'), (4, 'Aprobado'), (5, 'Valido para construcción'), (6, 'Aprobado (en numeracion)')], default=1),
        ),
        migrations.AlterField(
            model_name='version',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Creador'),
        ),
    ]
