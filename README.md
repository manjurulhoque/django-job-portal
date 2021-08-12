<div align="center">

<img src="./screenshots/illustration.png" alt="Job Interview" width="300" height="356.5">

# Django Job Portal

</div>

## Django Job Portal

#### An open source online job portal.

<p align="center">
    <img alt="forks" src="https://img.shields.io/github/forks/manjurulhoque/django-job-portal?label=Forks&style=social"/>
    <img alt="stars" src="https://img.shields.io/github/stars/manjurulhoque/django-job-portal?style=social"/>
    <img alt="watchers" src="https://img.shields.io/github/watchers/manjurulhoque/django-job-portal?style=social"/>
    <img alt="github Actions" src="https://github.com/manjurulhoque/django-job-portal/workflows/job-portal/badge.svg"/>
</p>

Live: [Demo](https://django-job.herokuapp.com/) or [Second Demo](http://jobs.manjurulhoque.com/)

Used Tech Stack

1. Django
2. Sqlite

### Screenshots

## Home page
<img src="screenshots/one.png" height="800">

## Login page
<img src="screenshots/five.png" height="800">

## Add new position as employer
<img src="screenshots/two.png" height="800">

## Job details
<img src="screenshots/three.png" height="800">

## Swagger API
<img src="screenshots/four.png" height="800">

<a name="local-venv"></a>
### Local environment

#### Install

1. Create a virtual environment

    `virtualenv venv`

    Or

    `python3.8 -m venv venv`

2. Activate it

    `source venv/bin/activate`

3. Clone the repository and install the packages in the virtual env:

    `pip install -r requirements.txt`

4. Add `.env` file.

    `cp .env.dev.sample .env`

5. Add Github client ID and client secret in the `.env` file

#### Run

1.With the venv activate it, execute:

    python manage.py collectstatic

*Note* : Collect static is not necessary when debug is True (in dev mode)

2. Create initial database:

    `python manage.py migrate`


3. Load demo data (optional):

    `python manage.py loaddata fixtures/app_name_initial_data.json --app app.model_name`

4. Run server:

    `python manage.py runserver`


#### Run test:
``python manage.py test``

#### To dump data:
``python manage.py dumpdata --format=json --indent 4 app_name > app_name/fixtures/app_name_initial_data.json``

Show your support by 🌟 the project!!
