#!/bin/bash
set -e

echo "Starting Django application..."

# Collecte des fichiers statiques (ne doit pas échouer)
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Tentative de migration (peut échouer si DB pas accessible)
echo "Attempting database migrations..."
python manage.py migrate --run-syncdb || echo "Migration failed, continuing..."

echo "Starting server on 0.0.0.0:8000..."
exec python manage.py runserver 0.0.0.0:8000