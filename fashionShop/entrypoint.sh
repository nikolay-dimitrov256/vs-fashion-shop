#!/bin/sh

echo "Running Django setup tasks..."

# Wait for DB (optional: only if your app starts before DB is ready)
echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do sleep 1; done
echo "PostgreSQL is up."

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Create staticfiles and media dirs if not exist
mkdir -p /app/staticfiles /media
chmod -R 777 /app/staticfiles /media

# Collect static files (optional in dev)
echo "Collecting static files..."
python3 manage.py collectstatic --noinput

# Compile translation files.
echo "Compiling .po to .mo..."
python manage.py compilemessages

# Run the main command passed to the container
echo "Switching to appuser..."
exec su appuser -c "$*"
