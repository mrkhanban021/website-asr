#!/bin/bash
set -e

echo "🗃️ Running database migrations..."
python manage.py migrate --noinput

echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput
python manage.py init_site_setting

echo "✅ Starting application..."
exec "$@"
