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

from .models import *
from .forms import *
from .serializers import *

import base64


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'index.html', {'form': form})
    
    def post(self, request):
        form = LoginForm(request.POST, request.FILES)
        # print(f'{request.POST}')
        # huella = request.FILES.get('huella')
        # print(huella.file)
        # miau = base64.b64encode(huella.file.getvalue())
        # print(miau)
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
    template_name = 'home.html'

    def get(self, request):
        print(f'{request.user=}')
        return super().get(request)
    
    
class ObtenerPacienteView(APIView):
    
    def get(self, request):
        curp = request.data.get('curp')
        
        print(f'{curp=}')
        
        huella = request.data.get('huella')
        print(huella)
        huella_base64 = base64.b64encode(huella.file.getvalue())
        
        paciente = Paciente.objects.get(curp=curp)
        
        huella_usuario = base64.b64encode(paciente.huella.file.read())
        if huella_base64 == huella_usuario:
            # get Expediente
            expediente = paciente.expediente
            cita = Cita.objects.filter(expediente=expediente).last()
            cita_serialized = CitaSerializer(cita)
            

            
            # consultas = Consulta.objects.filter(cita=cita)
            consultas = cita.consulta.all()
            consultas = ConsultaSerializer(consultas, many=True)
            
            imagen = Imagen.objects.filter(cita=cita)
            imagen = ImagensSerializer(imagen, many=True)
            
            laboratorio = Laboratorio.objects.filter(cita=cita)
            laboratorio = LaboratorioSerializer(laboratorio, many=True)
            
            
            miau = ExpedienteSerilizer(expediente)
            
            
            response = {'cita': cita_serialized.data, 'consultas': consultas.data, 'images': imagen.data, 'laboratorio': laboratorio.data}
            
            # response = {'expediente': miau.data}
            return Response(response, status=200)
            
            
            
        
        
        