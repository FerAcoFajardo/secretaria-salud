from rest_framework import serializers

from .models import *

class ExpedienteSerilizer(serializers.ModelSerializer):
    """Serializador para el modelo `core.Expediente`"""
    
    class Meta:
        model = Expediente
        fields = '__all__'

        
class CitaSerializer(serializers.ModelSerializer):
    """Serializador para el modelo `core.Cita`"""
    
    class Meta:
        model = Cita
        fields = '__all__'
        

class ConsultaSerializer(serializers.ModelSerializer):
    """Serializador para el modelo `core.Consulta`"""
    
    class Meta:
        model = Consulta
        fields = (
            'id',
            'comentarios_consulta',
            'usuario',
        )
        
        
class ImagensSerializer(serializers.ModelSerializer):
    """Serializador para el modelo `core.Imagen`"""
    
    class Meta:
        model = Imagen
        fields = (
            'id',
            'comentarios_imagen',
            'usuario',
            'imagen',
        )
        
        
class LaboratorioSerializer(serializers.ModelSerializer):
    """Serializador para el modelo `core.Laboratorio`"""
    
    class Meta:
        model = Laboratorio
        fields = '__all__'
        

class PacienteSerializer(serializers.ModelSerializer):
    """Serializador para el modelo `core.Paciente`"""
    
    class Meta:
        model = Paciente
        fields = '__all__'