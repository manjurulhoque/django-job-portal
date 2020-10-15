## Django Job Portal

#### An open source online job portal.

![Github Actions](https://github.com/manjurulhoque/django-job-portal/workflows/job-portal/badge.svg)

Live: [Demo](https://django-portal.herokuapp.com/) or [Second Demo](http://jobs.manjurulhoque.com/)

Used Tech Stack

1. Django
2. Sqlite

### Install

1. Create a virtual environment

   `virtualenv venv`

   Or

   `python3.8 -m venv venv`

2. Activate it

   `source venv/bin/activate`

3. Install the packages in the virtual env:

   `pip install -r requirements.txt`

4. Add `.env` file.

   `cp .env.dev.sample .env`

### Run

With the venv activate it, execute:

`python manage.py collectstatic`

_Note_ : Collect static is not necessary when debug is True (in dev mode)

Create initial database:

`python manage.py migrate`

Load demo data (optional):

`python manage.py loaddata demo`

Run server:

`python manage.py runserver 0.0.0.0:8000`

### Development Environment with Docker

If you wish to use a dockerized development environment, you can easily do so by following these steps:

1. Add `.env` file:

   `cp .env.dev.sample .env`

2. Start local development env:

   `make start`

   Or, if you wish to run in detached mode:

   `make serve`

3. Execute tests:

   `make tests`

4. To see all available options:

   `make help`

#### Development with docker dev environment

Once the environment is up and running, you can modify the project files and the
Django auto-reload will pick up your changes in the container.

To stop the dockerized development environment use:

`CTRL+C` or `make stop` if you run in detached mode.

#### Executing database migrations

The app container runs database migrations at every startup, so simply restart the app server with

`make restart c=app`

#### Changing requirements file

If during development you need to change the `requirements.txt` file you'll also have to rebuild the container:

1. Build images again with `make build` or `make build c=app` // or `c=test`

2. Stop and remove your environment with `make restart`. Even though containers are removed, your database volume will be preserved.

#### Recreate DB

If you want to recreate the DB just:

1. Delete everything including volumes with `make purge`

2. Restart everything with `make up` (or `make serve` for detached mode)

### Screenshots

## Home page

<img src="screenshots/one.png" height="800">

## Add new position as employer

<img src="screenshots/two.png" height="800">

## Job details

<img src="screenshots/three.png" height="800">

Show your support by 🌟 the project!!
