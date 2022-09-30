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
	pipenv run python manage.py migrate

.PHONY: makemigrations-test
makemigrations-test:
	cd ./backend && \
	pipenv run python manage.py makemigrations --dry-run


.PHONY: makemigrations
makemigrations:
	cd ./backend && \
	pipenv run python manage.py makemigrations

ARGPATH=.

.PHONY: test
test:
	clear
	docker-compose up --build db -d && \
	cd ./backend && \
	pipenv run pytest -k $(ARGPATH)

.PHONY: test-frontend
test-frontend:
	clear
	cd ./frontend && \
	npm test

.PHONY: mypy
mypy:
	clear
	cd ./backend/ && \
	pipenv run mypy . --config-file="../pyproject.toml"

.PHONY: oops
oops:
	rm -rf Pipfile Pipfile.lock ./venv

$PACKAGE = .

.PHONY: install
install:
	cd ./backend && \
	pipenv install $(PACKAGE)

.PHONY: shell
shell:
	cd ./backend && \
	pipenv run python manage.py shell

.PHONY: graph
graph:
	cd ./backend && \
	pipenv run python manage.py graph_models --rankdir BT api users -o my_project_visualised.png && \
	open my_project_visualised.png

.PHONY: actions
actions:
	act --container-architecture linux/amd64

.PHONY: generate-key
generate-key:
	@echo '' && \
	cd ./backend && \
	pipenv -q run python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'

.PHONY: serve-docs
serve-docs:
	cd ./backend && \
		pipenv run mkdocs serve --config-file ../mkdocs.yml
