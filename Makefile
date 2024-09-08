.PHONY: install migrate convert start selfcheck lint check 

MANAGE := poetry run python manage.py

install:
	poetry install --no-root

makemigrations:
	$(MANAGE) makemigrations

migrate:
	$(MANAGE) migrate

dev:
	$(MANAGE) runserver localhost:8030

convert:
	$(MANAGE) collectstatic --no-input

makemessages:
	$(MANAGE) makemessages -l ru

compilemessages:
	$(MANAGE) compilemessages --ignore=.venv

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.asgi:application -k uvicorn.workers.UvicornWorker

selfcheck:
	poetry check

lint:
	poetry run flake8 task_manager --exclude=*migrations/

test:
	poetry run pytest task_manager

check: selfcheck lint test
