## Django Job Portal

#### An open source online job portal.

![Github Actions](https://github.com/manjurulhoque/django-job-portal/workflows/job-portal/badge.svg)

Live: [Demo](https://django-portal.herokuapp.com/) or [Second Demo](http://jobs.manjurulhoque.com/)

Used Tech Stack

1. Django
2. Sqlite

### Screenshots

## Home page
<img src="screenshots/one.png" height="800">

## Add new position as employer
<img src="screenshots/two.png" height="800">

## Job details
<img src="screenshots/three.png" height="800">

#### Run test:
``python manage.py test``

#### To dump data:
``python manage.py dumpdata --format=json --indent 4 app_name > app_name/fixtures/app_name_initial_data.json``

#### To load data:
``python manage.py loaddata fixtures/app_name_initial_data.json --app app.model_name``

Show your support by 🌟 the project!!