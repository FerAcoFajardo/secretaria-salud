from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth import login
from django import forms


from .models import Usuario


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    cedula_profesional = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Cédula Profesional',
                                                                     'class': 'border w-full h-10 px-3 '
                                                                              'mb-5 rounded-md'}))

    huella = forms.CharField(widget=forms.FileInput(attrs={'placeholder': 'Huella',
                                                           'class': 'form-control block w-full px-5 py-1.5 text-base '
                                                                    'font-normal text-gray-700 w-full h-10 mb-14 pb-14'
                                                                    'bg-white bg-clip-padding border border-solid '
                                                                    'border-gray-300 rounded transition rounded-md'
                                                                    'ease-in-out m-0 focus:text-gray-700 '
                                                                    'focus:bg-white focus:border-blue-600 '
                                                                    'focus:outline-none'}))

    
    def authenticate(self, request):
        cedula_profesional = self.cleaned_data['cedula_profesional']
        huella = self.cleaned_data['huella']
        
        if cedula_profesional and huella:
            usuario = Usuario.objects.get(cedula_profesional=cedula_profesional, huella=huella)
            login(request, usuario)
            return usuario
        return None