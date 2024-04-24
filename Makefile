MANAGE := poetry run python manage.py

setup: install makemigrations migrate

install:
	poetry install --no-root

makemigrations:
	@$(MANAGE) makemigrations

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

compil:
	python manage.py compilemessages