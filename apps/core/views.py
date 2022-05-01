from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
# Create your views here.
from django.views.generic import TemplateView

from .models import *
from .forms import *

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
            
            
            # Huella to base64
            huella_dactilar = request.FILES.get('huella')
            huella_dactilar = base64.b64encode(huella_dactilar.file.getvalue())
            cedula_profesional = form.cleaned_data['cedula_profesional']
            
            form.huella = huella_dactilar
            
            resultado = form.authenticate(request)
            
            if resultado is None:
                return render(request, 'index.html', {'form': form, 'error': 'Usuario o contraseña incorrectos'})
        else:
            print(f'{form.errors=}')
            return render(request, 'index.html', {'form': form, 'error': 'Usuario o contraseña incorrectos'})
        return redirect(reverse_lazy('home'))


class HomeView(TemplateView):
    template_name = 'home.html'
