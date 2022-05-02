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
    usuario = Usuario.objects.first()
    
    
    # # Create Expediente
    # expediente = Expediente.objects.create(paciente=paciente)
    
    cita = Cita.objects.get(id=1)
    
    consultas = Consulta.objects.create(
        comentarios_consulta='Consulta 2',
        usuario=usuario,
        cita=cita
    )
    
    imagen = Imagen.objects.create(
        comentarios_imagen='Imagen 4',
        usuario=usuario,
        imagen='examenes/imagen2.png',
        cita=cita
    )
    imagen = Imagen.objects.create(
        comentarios_imagen='Imagen 5',
        usuario=usuario,
        imagen='examenes/imagen3.jpg',
        cita=cita
    )
    
    laboratorio = Laboratorio.objects.create(
        comentarios_laboratorio='Laboratorio 4',
        usuario=usuario,
        resultado_PDF='resultados/resultados2.jpg',
        cita=cita
    )
    laboratorio3 = Laboratorio.objects.create(
        comentarios_laboratorio='Laboratorio 5',
        resultado_PDF='resultados/resultados3.jpg',
        usuario=usuario,
        cita=cita
    )
