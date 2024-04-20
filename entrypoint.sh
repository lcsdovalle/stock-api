#!/bin/bash

# Function to check if PostgreSQL is ready
wait_for_db() {
    echo "Checking for DB readiness..."
    while ! nc -z db 5432; do   
        sleep 0.1
    done
    echo "DB is ready!"
}

# Call the function to ensure DB readiness
wait_for_db

# Change directory to where manage.py is located
cd /code/src

# Apply migrations
echo "Applying migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

cd ..
# Start Gunicorn
exec gunicorn src.api.wsgi:application --bind 0.0.0.0:8000
