.PHONY: run
run:
	docker-compose --env-file ./backend/.env up -d --build db
	cd ./backend && pipenv run python manage.py runserver

.PHONY: migrate
migrate:
	cd ./backend && \
	pipenv run python manage.py collectstatic && \
	pipenv run python manage.py makemigrations && \
	pipenv run python manage.py migrate

.PHONY: test
test:
	cd ./backend && pipenv run pytest -vv
