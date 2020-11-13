#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z 0.0.0.0 5432; do
  sleep 0.5
  echo "wait..."
done

echo "PostgreSQL started"


sleep 5
python3 manage.py makemigrations
python3 manage.py migrate
uwsgi --socket :8000 --module project.wsgi -b 32768 & celery worker -A project.celery -B & daphne -b 0.0.0.0 -p 8001 project.asgi:application

exec "$@"