MANAGE := poetry run python manage.py

setup: install migrate

install:
	poetry install --no-root

migrate:
	@$(MANAGE) migrate

dev:
	python manage.py runserver

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi:application

lint:
	poetry run flake8 task_manager

test:
	python manage.py test