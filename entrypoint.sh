#!/usr/bin/env bash

set -e

echo "🔄 Run migrations..."
python manage.py migrate

echo "🔄 Collection statics..."
python manage.py collectstatic --no-input

echo "🔄 Load test data..."
python ./load_test_data/load_data.py

echo "🚀 Run application..."
uvicorn service_cash_manager.asgi:application --host 0.0.0.0 --port 8000 --workers 4
