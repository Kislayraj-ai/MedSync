import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()

# Compute project root (one level above config/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_ROOT = os.path.abspath(STATIC_ROOT)

application = WhiteNoise(
    application,
    root=STATIC_ROOT,
    prefix='/static/',  # must match STATIC_URL
)
