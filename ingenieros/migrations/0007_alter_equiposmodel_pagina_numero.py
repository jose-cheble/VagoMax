# Generated by Django 4.0.3 on 2022-04-06 01:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingenieros', '0006_rename_insepeccionesmodel_inspeccionesmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equiposmodel',
            name='pagina_numero',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(11), django.core.validators.MaxValueValidator(46)]),
        ),
    ]
