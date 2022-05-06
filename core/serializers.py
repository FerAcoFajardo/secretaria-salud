from rest_framework import serializers

from .models import *

class ExpedienteSerilizer(serializers.ModelSerializer):

    
    class Meta:
        model = Expediente
        fields = '__all__'

        
class CitaSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Cita
        fields = '__all__'
        

class ConsultaSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Consulta
        fields = (
            'id',
            'comentarios_consulta',
            'usuario',
        )
        
        
class ImagensSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Imagen
        fields = (
            'id',
            'comentarios_imagen',
            'usuario',
            'imagen',
        )
        
        
class LaboratorioSerializer(serializers.ModelSerializer):
        
    
    class Meta:
        model = Laboratorio
        fields = '__all__'
        

class PacienteSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Paciente
        fields = '__all__'