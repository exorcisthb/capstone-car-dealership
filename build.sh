#!/usr/bin/env bash
set -o errexit

echo "=== Installing dependencies ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== Running Django system check ==="
cd server
python manage.py check

echo "=== Running migrations ==="
python manage.py migrate --noinput

echo "=== Seeding initial data (dealers, car makes, reviews, testuser) ==="
python manage.py seed_data

echo "=== Collecting static files ==="
python manage.py collectstatic --noinput

echo "=== Build complete ==="
