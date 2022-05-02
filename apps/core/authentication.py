from django.contrib.auth.backends import BaseBackend
from .models import Usuario

class MyBackend(BaseBackend):
    def authenticate(self, request, cedula_profesional=None, huella=None):
        
        if cedula_profesional and huella:
            usuario = Usuario.objects.get(cedula_profesional=cedula_profesional, huella=huella)
            return usuario
        else:
            return None