.PHONY: run
run:
	pipenv run python manage.py runserver

.PHONY: migrate
migrate:
	pipenv run python manage.py makemigrations
	pipenv run python manage.py migrate