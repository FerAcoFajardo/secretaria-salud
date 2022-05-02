# Generated by Django 4.0.2 on 2022-05-02 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_cita_expediente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='sexo',
            field=models.CharField(blank=True, choices=[('MASCULINO', 'Masculino'), ('FEMENINO', 'Femenino'), ('OTRO', 'Otro')], max_length=30, null=True, verbose_name='Sexo'),
        ),
    ]
