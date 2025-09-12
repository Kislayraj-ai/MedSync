"""
WSGI config for web_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from whitenoise import WhiteNoise

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()

# Serve static files using Whitenoise
# Serve static files
STATIC_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../staticfiles')
application = WhiteNoise(application, root=STATIC_ROOT, prefix='/static/')