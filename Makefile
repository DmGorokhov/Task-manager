install:
		poetry install

dev:
		poetry run python manage.py runserver

lint:
		poetry run flake8 task_manager
