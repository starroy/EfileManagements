#!/bin/bash
cd /code
# systemctl disable mysql
systemctl enable mysql --now
export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_PASSWORD=admin123
# python3 manage.py migrate;
#
python3 manage.py makemigrations
#
python3 manage.py migrate
#
# python3 manage.py collectstatic --clear;

# python3 manage.py createsuperuser --no-input || true;
# python3 create_admin.py
python manage.py collectstatic
python manage.py runserver 0.0.0.0:8000
# python manage.py runserver_plus --cert-file cert.pem --key-file key.pem 0.0.0.0:8000 
# gunicorn core.wsgi --bind 0.0.0.0:8000

