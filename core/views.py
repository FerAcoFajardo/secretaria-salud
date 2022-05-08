from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
# Create your views here.
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.contrib.auth.hashers import make_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from oauth2_provider.models import AccessToken
from oauth2_provider.models import Application


from core.models import *
from core.forms import *
from core.serializers import *

import base64, json
from datetime import datetime
import requests

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
    
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

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
                return Response({'Error': 'Cita no encontrada'}, status=status.HTTP_418_IM_A_TEAPOT)

            
            
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
            return Response(response, status=status.HTTP_200_OK)
            

class LoginAPIView(APIView):
    
    def post(self, request):
        
        data = request.data
        cedula_profesional = data.get('cedula_profesional')
        huella = data.get('huella')
        huella_base64 = base64.b64encode(huella.file.getvalue())
        if cedula_profesional and huella:
            usuario = Usuario.objects.get(cedula_profesional=cedula_profesional)
            huella_usuario = base64.b64encode(usuario.huella.file.read())
            if huella_base64 == huella_usuario:
                token = Token.objects.get_or_create(user=usuario)[0]
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'Message': 'Cedula o huella no coinciden'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Message': 'Faltan datos'}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        return Response({'Message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def put(self, request):
        return Response({'Message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def patch(self, request):
        return Response({'Message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def delete(self, request):
        return Response({'Message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    
class OauthLoginAPIView(APIView):
    
    def post(self, request):
        data = request.data
        cedula_profesional = data.get('cedula_profesional')
        # huella = data.get('huella')
        # huella_base64 = base64.b64encode(huella.file.getvalue())
        password = data.get('password')
        print(password)
        password = make_password(password)
        
        # if cedula_profesional and huella:
        usuario = Usuario.objects.get(cedula_profesional=cedula_profesional)
        
        print(usuario.password)
        print(password)
        # huella_usuario = base64.b64encode(usuario.huella.file.read())
        # if huella_base64 == huella_usuario:
        token = AccessToken.objects.filter(user=usuario, expires__gt=datetime.now())
        if token:
            token = token.first()
            token = token.token
            return Response({'token': token.token}, status=status.HTTP_200_OK)
        else:
            if not Application.objects.filter(user=usuario.id).exists():
                Application.objects.create(user=usuario.id, authorization_grant_type='password', client_type='confidential')
            app = Application.objects.filter(user=usuario.id).first()
            if app:
                url = f'http://{request.get_host()}/o/token/'
                # print(url)
                client_id = app.client_id
                client_secret = app.client_secret
                data_dict = {"grant_type": "password", "username": cedula_profesional, "password": password, "client_id": client_id, "client_secret": client_secret}
                # print(data_dict)
                aa = requests.post(url, data=data_dict)
                data = json.loads(aa.text)
                print(data)
                token = data.get('access_token', '')
                return Response({'token': token}, status=status.HTTP_200_OK)
        # else:
            # return Response({'Message': 'Cedula o huella no coinciden'}, status=status.HTTP_400_BAD_REQUEST)
        
        
class CreatePasswordAPIView(APIView):
    def post(self, request):
        data = request.data
        password = data.get('password')
        print(password)
        password = make_password(password)
        
        return Response({'password': password}, status=status.HTTP_200_OK)