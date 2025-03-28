"""
WSGI config for rate_a_leg_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

load_dotenv('/home/RossS/RateALeg/.env')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rate_a_leg_project.settings')
application = get_wsgi_application()