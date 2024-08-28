install:
	poetry install

migrate:
	poetry run python manage.py migrate

convert:
	poetry run python manage.py collectstatic --no-input

start:
	poetry run python manage.py runserver 0.0.0.0:8000

selfcheck:
	poetry check

lint:
	poetry run flake8 task_manager

check: selfcheck lint

PHONY: install migrate convert start selfcheck lint check
