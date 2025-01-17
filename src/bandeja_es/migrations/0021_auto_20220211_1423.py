# Generated by Django 3.1.1 on 2022-02-11 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bandeja_es', '0020_auto_20220209_0042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prevversion',
            name='prev_revision',
            field=models.IntegerField(blank=True, choices=[('', '------'), (1, 'B'), (2, 'C'), (3, 'D'), (4, 'E'), (5, '0'), (6, '1'), (7, '2'), (8, '3'), (9, '4'), (10, '5'), (11, 'A')], verbose_name='Revisión'),
        ),
        migrations.AlterField(
            model_name='version',
            name='revision',
            field=models.IntegerField(blank=True, choices=[('', '------'), (1, 'B'), (2, 'C'), (3, 'D'), (4, 'E'), (5, '0'), (6, '1'), (7, '2'), (8, '3'), (9, '4'), (10, '5'), (11, 'A')], verbose_name='Revisión'),
        ),
    ]
