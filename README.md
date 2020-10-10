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

    `cd jobs/settings`

    `cp .env.dev.sample .env`

### Run
With the venv activate it, execute:

`python manage.py collectstatic`

*Note* : Collect static is not necessary in dev mode

`python manage.py runserver 0.0.0.0:8000`

### Screenshots

## Home page
<img src="screenshots/one.png" height="800">

## Add new position as employer
<img src="screenshots/two.png" height="800">

## Job details
<img src="screenshots/three.png" height="800">

Show your support by 🌟 the project!!
