#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Creating media directory..."
mkdir -p media/logos

echo "Running migrations..."
python manage.py migrate

echo "Build completed successfully!"
