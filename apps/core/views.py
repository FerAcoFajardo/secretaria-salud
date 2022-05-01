from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
# Create your views here.
from django.views.generic import TemplateView

from .models import *
from .forms import *


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'index.html', {'form': form})


class HomeView(TemplateView):
    template_name = 'home.html'
