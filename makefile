.PHONY: run
run:
	docker-compose --env-file ./backend/.env up -d --build db cd ./backend && pipenv run python manage.py runserver

.PHONY: migrate
migrate:
	cd ./web/backend && \
	pipenv run python manage.py collectstatic && \
	pipenv run python manage.py makemigrations && \
	pipenv run python manage.py migrate

.PHONY: test
test:
	cd ./web/backend && pipenv run pytest -vv

.PHONY: pipinstall
pipinstall:
	cd ./web/backend && pipenv install $(packages)