#!/bin/bash
# pipenv run python manage.py makemigrations --no-input
# pipenv run python manage.py migrate
# pipenv run python manage.py collectstatic --no-input

pipenv run python manage.py runserver 0.0.0.0:8000
