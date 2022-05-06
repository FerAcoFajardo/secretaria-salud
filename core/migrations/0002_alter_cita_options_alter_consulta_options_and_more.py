# Generated by Django 4.0.2 on 2022-05-01 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cita',
            options={'ordering': ['fecha'], 'verbose_name': 'Cita', 'verbose_name_plural': 'Citas'},
        ),
        migrations.AlterModelOptions(
            name='consulta',
            options={'verbose_name': 'Consulta', 'verbose_name_plural': 'Consultas'},
        ),
        migrations.AlterModelOptions(
            name='expediente',
            options={'ordering': ['paciente'], 'verbose_name': 'Expediente', 'verbose_name_plural': 'Expedientes'},
        ),
        migrations.AlterModelOptions(
            name='imagen',
            options={'verbose_name': 'Imagen', 'verbose_name_plural': 'Imagenes'},
        ),
        migrations.AlterModelOptions(
            name='laboratorio',
            options={'ordering': ['id'], 'verbose_name': 'Laboratorio', 'verbose_name_plural': 'Laboratorios'},
        ),
        migrations.AlterModelOptions(
            name='paciente',
            options={'ordering': ['nombre'], 'verbose_name': 'Paciente', 'verbose_name_plural': 'Pacientes'},
        ),
        migrations.AlterModelOptions(
            name='usuario',
            options={'ordering': ['cedula_profesional'], 'verbose_name': 'Usuario', 'verbose_name_plural': 'Usuarios'},
        ),
        migrations.AlterModelManagers(
            name='usuario',
            managers=[
            ],
        ),
        migrations.RenameField(
            model_name='laboratorio',
            old_name='resultadoPDF',
            new_name='resultado_PDF',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='email',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='user_permissions',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='username',
        ),
        migrations.AlterField(
            model_name='usuario',
            name='cedula_profesional',
            field=models.CharField(max_length=50, unique=True, verbose_name='Cedula profesional'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='correo',
            field=models.EmailField(max_length=50, unique=True, verbose_name='Correo'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='huella',
            field=models.CharField(max_length=99999, unique=True, verbose_name='Huella'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='is_superuser',
            field=models.BooleanField(default=False, verbose_name='Es superusuario'),
        ),
        migrations.AlterModelTable(
            name='cita',
            table='cita',
        ),
        migrations.AlterModelTable(
            name='consulta',
            table='consulta',
        ),
        migrations.AlterModelTable(
            name='expediente',
            table='expediente',
        ),
        migrations.AlterModelTable(
            name='imagen',
            table='imagen',
        ),
        migrations.AlterModelTable(
            name='laboratorio',
            table='laboratorio',
        ),
        migrations.AlterModelTable(
            name='paciente',
            table='paciente',
        ),
        migrations.AlterModelTable(
            name='usuario',
            table='usuario',
        ),
    ]