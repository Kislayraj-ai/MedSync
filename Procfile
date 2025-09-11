web: gunicorn config.wsgi
web: python manage.py collectstatic --noinput && gunicorn medsync.wsgi:application