"""
WSGI config for TechnoTickets project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import pathlib
from dotenv import load_dotenv


from django.core.wsgi import get_wsgi_application

CURENT_DIR = pathlib.Path(__file__).resolve().parent
BASE_DIR = CURENT_DIR.parent
ENV_FILE_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=str(ENV_FILE_PATH))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TechnoTickets.settings')

application = get_wsgi_application()
