# Generated by Django 3.1.1 on 2021-03-08 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel_carga', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revision',
            name='tipo',
            field=models.IntegerField(choices=[('', '------'), (1, 'B'), (2, 'C'), (3, 'D'), (4, 'E'), (5, '0'), (6, '1'), (7, '2'), (8, '3'), (9, '4'), (10, '5')], verbose_name='Tipo Revision'),
        ),
    ]
