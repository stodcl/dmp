# Generated by Django 3.1.1 on 2021-05-03 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bandeja_es', '0006_auto_20210326_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='version',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='proyecto/documentos/'),
        ),
    ]