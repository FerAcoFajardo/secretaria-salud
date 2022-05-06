from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
# Create your views here.
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.models import *
from core.forms import *
from core.serializers import *

import base64


class LoginView(View):
    """ View para el login

        model `core.Usuario`
        template `index.html`
    """
    def get(self, request):
        """ Función get, para manejar las peticiones get del cliente
        
            Esta función se encarga de renderizar el html de la página de login

            Args:
                request (HttpRequest): Peticion del cliente
            Returns:
                HttpResponse: Respuesta del servidor
        """
        form = LoginForm()
        return render(request, 'index.html', {'form': form})
    
    def post(self, request):
        """ Función de post, para manejar las peticiones post del cliente

            Args:
                request (HttpRquest): Petición del cliente

            Esta función se encarga de validar el formulario de login e iniciar la sesión del usuario despues lo redirecciona a la página de inicio
            
            Returns:
                HttpResponse: Respuesta del servidor
        """
        form = LoginForm(request.POST, request.FILES)

        if form.is_valid():
            print(f'Entro al formulario')
            
            cedula_profesional = form.cleaned_data['cedula_profesional']
            huella = request.FILES.get('huella')
            
            huella_base64 = base64.b64encode(huella.file.getvalue())
            
            if cedula_profesional and huella:
                
                usuario = Usuario.objects.get(cedula_profesional=cedula_profesional)
                huella_usuario = base64.b64encode(usuario.huella.file.read())
                if huella_base64 == huella_usuario:
                    login(request, usuario)
                    return redirect(reverse_lazy('home'))
                return render(request, 'index.html', {'form': form, 'error': 'Usuario o contraseña incorrectos'})
        else:
            print(f'{form.errors=}')
            return render(request, 'index.html', {'form': form, 'error': 'Usuario o contraseña incorrectos'})
        return redirect(reverse_lazy('home'))


class HomeView(LoginRequiredMixin, TemplateView):
    """ View de home
    
        View que se encarga de renderizar la página de inicio
    
        template: `home.html`
    """
    template_name = 'home.html'

    def get(self, request):
        """ Función get, para manejar las peticiones get del cliente
            Renderiza la página de inicio
            Regresa una respuesta del servidor
        """
        return super().get(request)
    
    
class ObtenerPacienteView(APIView):
    """ View para obtener la información del paciente
    """
    def post(self, request):
        """ Función post, para manejar las peticiones post del cliente
        
            Esta función obtiene toda la información del paciente
        
            Args:
                request (HttpRequest): Petición del cliente
        """
        curp = request.data.get('curp') # Curp del paciente
        response = {} # Creación de json para la respuesta
        
        
        huella = request.data.get('huella') # Huella del paciente
        huella_base64 = base64.b64encode(huella.file.getvalue()) # Huella del paciente en base64
        
        paciente = Paciente.objects.get(curp=curp) # Consulta del paciente
        
        huella_usuario = base64.b64encode(paciente.huella.file.read()) # Huella del paciente en base64
        # Comparación de las huellas
        if huella_base64 == huella_usuario:
            # Serialización de los datos del paciente a bnse64
            paciente_serialized = PacienteSerializer(paciente)
            # Agregación de la información del paciente a la respuesta
            response['paciente'] = paciente_serialized.data
            # Consultando el expediente del paciente
            expediente = paciente.expediente
            # Try para obtener la cita
            try:
                # Consultando la cita del paciente
                cita = Cita.objects.filter(expediente=expediente).last()
                # Serialización de la cita
                cita_serialized = CitaSerializer(cita)
                # Agregación de la cita a la respuesta
                response['cita'] = cita_serialized.data
            except Cita.DoesNotExist:
                # Si no existe la cita, se envia mensaje de error con el estatus 418
                return Response({'Error': 'Cita no encontrada'}, status=418)

            
            
            try:
                # Consultando todas las consultas del paciente
                consultas = cita.consulta.all()
                # Serialización de las consultas
                consultas = ConsultaSerializer(consultas, many=True)
                # Agregación de las consultas a la respuesta
                response['consultas'] = consultas.data
            except Consulta.DoesNotExist:
                pass 
            
            try:
                # Consultando todos los examenes del paciente
                imagen = Imagen.objects.filter(cita=cita)
                # Serialización de los examenes
                imagen = ImagensSerializer(imagen, many=True)
                # Agregación de los examenes a la respuesta
                response['images'] = imagen.data
            except Imagen.DoesNotExist:
                pass
            
            try:
                # Consultando todos los análisis del paciente
                laboratorio = Laboratorio.objects.filter(cita=cita)
                # Serialización de los análisis
                laboratorio = LaboratorioSerializer(laboratorio, many=True)
                # Agregación de los análisis a la respuesta
                response['laboratorios'] = laboratorio.data
            except Laboratorio.DoesNotExist:
                pass
            
            # Se regresa la respuesta del servidor
            return Response(response, status=200)
            
            
            
        
        
        