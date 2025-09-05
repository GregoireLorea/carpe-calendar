#!/bin/bash
set -e

echo "Starting Django application..."

# Collecte des fichiers statiques (ne doit pas échouer)
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Tentative de migration (peut échouer si DB pas accessible)
echo "Attempting database migrations..."
python manage.py migrate --run-syncdb || echo "Migration failed, continuing..."

# Test de connexion DB avant de démarrer le serveur
echo "Testing database connection..."
python manage.py check --database default || echo "Database check failed, but continuing..."

PORT=${PORT:-8000}
echo "PORT environment variable: $PORT"
echo "Starting server on 0.0.0.0:${PORT}..."

# S'assurer que le port est bien numérique  
case "$PORT" in
    ''|*[!0-9]*) 
        echo "Error: PORT is not a number: $PORT"
        PORT=8000
        echo "Using default PORT: $PORT"
        ;;
    *) 
        echo "PORT is valid: $PORT"
        ;;
esac

exec python manage.py runserver 0.0.0.0:${PORT} --noreload