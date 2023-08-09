MANAGE := poetry run python manage.py

install:
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

test:
		poetry run ./manage.py test

test-cov:
		poetry run coverage run ./manage.py test

shell:
		poetry run ./manage.py shell