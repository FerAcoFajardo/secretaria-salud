from django.db import transaction
from django.core.management.base import BaseCommand

from ...models import *

from datetime import datetime


class Command(BaseCommand):
    help = 'Seed database with users'

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help='Mode')

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed()
        self.stdout.write('done.')
        
        
def run_seed():
    usuario = Usuario.objects.create(
        cedula_profesional='1234',
        huella='huellas/huella.jpg',
        nombre='Dr. Pedro Picapiedra',
        correo='pedro@doctor.com',
        telefono='0426-1234567',
        is_superuser=True,
        is_active=True,
        is_staff=True
    )
    
    
    # Create Paciente
    paciente = Paciente.objects.create(
        nombre='Paciente 1',
        fecha_nacimiento=datetime.now(),
        curp='123456789012345678',
        huella='huellas/huella.jpg',
        correo='paciente@paciente.com',
        telefono='123456789',
        tipo_sangre='AP',
        sexo = 'MASCULINO',
        es_menor=False
    )
    
    
        
    
    # Create Expediente
    expediente = Expediente.objects.create(paciente=paciente)
    
    cita = Cita.objects.create(
        comentario='Cita 1',
        fecha=datetime.now(),
        usuario = usuario,
        expediente=expediente
    )
    
    consultas = Consulta.objects.create(
        comentarios_consulta='Consulta 1',
        usuario=usuario,
        cita=cita
    )
    
    imagen = Imagen.objects.create(
        comentarios_imagen='Imagen 1',
        usuario=usuario,
        imagen='examenes/imagen.jpg',
        cita=cita
    )
    imagen = Imagen.objects.create(
        comentarios_imagen='Imagen 2',
        usuario=usuario,
        imagen='examenes/imagen.jpg',
        cita=cita
    )
    imagen = Imagen.objects.create(
        comentarios_imagen='Imagen 3',
        usuario=usuario,
        imagen='examenes/imagen.jpg',
        cita=cita
    )
    
    laboratorio = Laboratorio.objects.create(
        comentarios_laboratorio='Laboratorio 1',
        usuario=usuario,
        resultado_PDF='resultados/resultados.jpg',
        cita=cita
    )
    laboratorio3 = Laboratorio.objects.create(
        comentarios_laboratorio='Laboratorio 3',
        resultado_PDF='resultados/resultados.jpg',
        usuario=usuario,
        cita=cita
    )
    laboratorio2 = Laboratorio.objects.create(
        comentarios_laboratorio='Laboratorio 2',
        resultado_PDF='resultados/resultados.jpg',
        usuario=usuario,
        cita=cita
    )