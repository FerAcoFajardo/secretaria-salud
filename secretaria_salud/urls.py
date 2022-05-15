"""secretaria_salud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
"""
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.urls import include, path, re_path
from django.contrib.admin.views.decorators import staff_member_required

from core.views import *

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.documentation import include_docs_urls
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('', LoginView.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('get-info/', ObtenerPacienteView.as_view(), name='obtener'),
    path('api/login/', LoginAPIView.as_view(), name='login-api'),
    path('make-password/',CreatePasswordAPIView.as_view(), name='make-password'),
    path('api/paciente/', ListCreatePacienteAPIView.as_view(), name='paciente-api'),
    path('docs/', include_docs_urls(title='Secretaria Salud API')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    
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
