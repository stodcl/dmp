# Generated by Django 3.1.1 on 2022-02-09 03:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bandeja_es', '0019_auto_20211118_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paqueteattachment',
            name='paquete',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='bandeja_es.paquete', verbose_name='Paquete'),
        ),
    ]
