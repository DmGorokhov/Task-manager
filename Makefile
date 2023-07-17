MANAGE := poetry run python manage.py

install: .env
		@poetry install

make-migration:
		@$(MANAGE) makemigrations

migrate: make-migration
		@$(MANAGE) migrate

build: install migrate

dev:
		poetry run python manage.py runserver

lint:
		poetry run flake8 task_manager
