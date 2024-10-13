[//]: # (### Hexlet tests and linter status:)
[![Actions Status](https://github.com/alex-j-fox/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/alex-j-fox/python-project-52/actions)
[![Actions Status](https://github.com/alex-j-fox/python-project-52/actions/workflows/django_ci.yml/badge.svg)](https://github.com/alex-j-fox/python-project-52/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/fac9194c877d8646a83e/maintainability)](https://codeclimate.com/github/alex-j-fox/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/fac9194c877d8646a83e/test_coverage)](https://codeclimate.com/github/alex-j-fox/python-project-52/test_coverage)

## Task manager
#### [Try task manager in live](https://python-project-52-5w5u.onrender.com)

### Description

A task management web application built with Python
and Django framework. It allows you to set
tasks, assign executors and change their statuses. Registration and
authentication are required to work with the system.

### Features

* Set tasks;
* Filter the tasks displayed by executors, author, labels and status;
* User authentication and registration;
* Change task status;
* Set multiple tasks labels;
* Assign executors;

### How to install

Clone the project:

    git clone https://github.com/alex-j-fox/python-project-52.git && cd python-project-52

Create .env file in the root folder and add following variables:

    SECRET_KEY = '{your secret key}' // Django secret key

If you want to use PostgreSQL:

    DATABASE_URL = postgresql://{provider}://{user}:{password}@{host}:{port}/{db}

If you choose to use SQLite, do not add DATABASE_URL variable.

For Rollbar errors tracking:

    ROLLBAR_ACCESS_TOKEN = '{token}'

Then install dependencies and create the tables in the database:

    make build

If you want create superuser:

    make create_superuser

## How to use it

Start the gunicorn server by running (UNIX) :

    make start

The server url will be at terminal, for example http://0.0.0.0:8000 or on PAAS server.
___________
Or start the development mode:

    make dev

The server url will be at terminal, for example http://127.0.0.1:8000.

### Deploy
###### If you want deploy your project, you may to follow these instructions [Render.com deploy instruction ](./static/docs/RENDER_DEPLOY.md)*(ru)*