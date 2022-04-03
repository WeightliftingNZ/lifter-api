.PHONY: run
run:
	docker-compose up --build db -d && \
	cd ./backend && \
	pipenv run python manage.py runserver

.PHONY: run-frontend
run-frontend:
	cd ./frontend && \
	npm start

.PHONY: migrate
migrate:
	cd ./backend && \
	pipenv run python manage.py makemigrations && \
	pipenv run python manage.py migrate
