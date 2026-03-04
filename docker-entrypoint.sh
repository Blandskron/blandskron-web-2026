#!/bin/sh
set -e

# Apply database migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if requested via env vars
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
	echo "Creating superuser $DJANGO_SUPERUSER_USERNAME (if not exists)..."
	python manage.py shell <<'PY'
from django.contrib.auth import get_user_model
import os
User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
if not User.objects.filter(username=username).exists():
		User.objects.create_superuser(username=username, email=email, password=password)
		print('Superuser created:', username)
else:
		print('Superuser already exists:', username)
PY
else
	echo "DJANGO_SUPERUSER_USERNAME or DJANGO_SUPERUSER_PASSWORD not provided; skipping superuser creation"
fi

echo "Starting Gunicorn..."
exec gunicorn blandskron.wsgi:application --bind 0.0.0.0:8000 --workers 3
