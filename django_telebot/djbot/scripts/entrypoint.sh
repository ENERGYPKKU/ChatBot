#!/usr/bin/env bash

set -e

echo "Collect static files"
python manage.py collectstatic --noinput

echo "Apply database migrations"
python manage.py makemigrations

python manage.py makemigrations main

python manage.py migrate --noinput

python manage.py runserver 0.0.0.0:8000 && python manage.py bot

uwsgi --strict --ini /app/uwsgi/uwsgi.ini

