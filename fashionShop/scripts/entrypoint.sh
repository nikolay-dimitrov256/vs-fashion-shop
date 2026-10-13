#!/bin/sh

set -e

if [ "$1" = "gunicorn" ]; then

    chown -R appuser:appuser /app/staticfiles

    echo "Running Django setup tasks..."

    # Apply database migrations
    echo "Applying database migrations..."
    gosu appuser python manage.py migrate --noinput

    # Collect static files (optional in dev)
    echo "Collecting static files..."
    gosu appuser python manage.py collectstatic --noinput

fi

# Execute the command passed as CMD in the Dockerfile or docker-compose.yml
exec gosu appuser "$@"
