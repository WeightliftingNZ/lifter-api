#!bin/sh
python manage.py collectstatic --no-input
python manage.py migrate
gunicorn --worker-tmp-dir /dev/shm config.wsgi -b 0.0.0.0:8000
