"""
WSGI config for secretaria_salud project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv
from dj_static import Cling

# Esto nomas lo cambia Claudio desde el servidor de produccion.
# BASE_DIR = "/home/claudio/deploys/xxx" 
# sys.path.append(BASE_DIR)
# sys.path.append(BASE_DIR+'venv/lib/python3.8/site-packages')
# load_dotenv(os.path.join(BASE_DIR, '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secretaria_salud.settings')

# application = get_wsgi_application()

application = Cling(get_wsgi_application())