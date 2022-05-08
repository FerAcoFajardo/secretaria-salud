"""secretaria_salud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.urls import include, path
# from apps.users import views as users_views
from django.contrib.admin.views.decorators import staff_member_required
from core.views import *

# from exampleApp.views import IndexExample

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('', LoginView.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('get-info/', ObtenerPacienteView.as_view(), name='obtener'),
    path('api/login/', LoginAPIView.as_view(), name='login-api'),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('oauth/login/', OauthLoginAPIView.as_view(), name='login-oauth'),
    path('make-password/',CreatePasswordAPIView.as_view(), name='make-password'),
    
    
    # User and Registration urls
    # path('', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    # path('profile/', users_views.ProfileView.as_view(), name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('register/', users_views.RegisterView.as_view(), name='register'),
    # path('register-admin/', staff_member_required(users_views.RegisterViewAdmin.as_view()), name='registerAdmin'),

    # path('forgot-password/', users_views.forgot_password, name='forgot-password'),
    path('users/', include('users.urls')),
    # path("__reload__/", include("django_browser_reload.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
