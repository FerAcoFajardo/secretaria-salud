# Generated by Django 4.0.2 on 2022-05-15 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_usuario_groups_usuario_user_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='curp',
            field=models.CharField(max_length=18, unique=True, verbose_name='CURP'),
        ),
    ]
