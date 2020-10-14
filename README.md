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

*Note* : Collect static is not necessary when debug is True (in dev mode)

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

2. Add `docker/.env` file for env override when running in container

   `cp docker/.env.dev.sample docker/.env`

3. Build the development image:

    `docker-compose build`

4. Run the development database and server:

    `docker-compose up`

    Or, if you wish to run in detached mode:

    `docker-compose up -d`

#### Development with docker dev environment

Once the environment is up and running, you can modify the project files and the
Django auto-reload will pick up your changes in the container.

To stop the dockerized development environment use:

`CTRL+C` or `docker-compose stop` if you run in detached mode.

#### Executing database migrations

The app container runs database migrations at every startup, so simply restart the app server with

`docker-compose restart app`

#### Changing requirements file

If during development you need to change the `requirements.txt` file you'll also have to rebuild the container:

1. Stop and remove your environment with `docker-compose down`. Even though containers are removed, your database volume will be preserved.

2. Build the container image again with `docker-compose build`

3. Restart development containers with `docker-compose up`


### Screenshots

## Home page
<img src="screenshots/one.png" height="800">

## Add new position as employer
<img src="screenshots/two.png" height="800">

## Job details
<img src="screenshots/three.png" height="800">

Show your support by 🌟 the project!!
