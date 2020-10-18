<h1 align="center">Anem per feina</h1>
<p align="center">
    <img alt="forks" src="https://img.shields.io/github/forks/GeeksCAT/anem-per-feina?label=Forks&style=social"/>
    <img alt="stars" src="https://img.shields.io/github/stars/GeeksCAT/anem-per-feina?style=social"/>
    <img alt="watchers" src="https://img.shields.io/github/watchers/GeeksCAT/anem-per-feina?style=social"/>
</p>

**Anem per feina** is an open source project promoted by [GeeksCat](https://geekscat.org/) association for [Hactoberfest 2020](https://hacktoberfest.geekscat.org/) event.

Show your support by 🌟 the project!!

* [The project](#the-project)
* [Contributing](#contributing)
* [Tech stack](#tech-stack)
* [Setup backend development environment](#setup-backend-development-environment)
  * [Docker](#docker)
  * [Local venv](#local-venv)
* [Screenshots](#screenshots)

<a name="the-project"></a>
## The project

The objective of this _hackathon_ is to launch a **job portal website** where tech community can find _curated_ job opportunities from local companies.

We forked the open source project [django-job-portal](https://github.com/manjurulhoque/django-job-portal) (See [demo 1](https://django-portal.herokuapp.com/), [demo 2](http://jobs.manjurulhoque.com/)) and use it as a baseline.


<a name="contributing"></a>
## Contributing

**Anem per feina** is a collaborative effort where everybody is more than welcome to contribute, no experience is required!

Have a look at [CONTRIBUTING.md](CONTRIBUTING.md) file that describes the process to submit a contribution, and come say hi 👋👋to [GeeksCat slack](https://geekscat.slack.com) where most contributors hang out.

<a name="tech-stack"></a>
## Tech stack

* **[Backend:](https://github.com/GeeksCAT/anem-per-feina)** A [django](https://www.djangoproject.com/) web application on top of a [PostgreSQL](https://www.postgresql.org/) database. It contains all business logic, data model (ORM) and a [django-rest-framework](https://www.django-rest-framework.org/) REST API to power the frontend/UI
* **Frontend:** A **[frontoffice](https://github.com/GeeksCAT/anem-per-feina-frontoffice)** using [vue.js](https://vuejs.org/)/[SASS](https://sass-lang.com/) using [BEMIT Architecture](https://csswizardry.com/2015/08/bemit-taking-the-bem-naming-convention-a-step-further/) and [Nuxt](https://nuxtjs.org/), and a **[backoffice](https://github.com/GeeksCAT/anem-per-feina-backoffice)** using [React](https://reactjs.org/)/[styled-components](https://styled-components.com/) and [Next](https://nextjs.org/)
* **Arch-ci:** Dockerized dev environment, CI/CD workflow and Kubernettes cluster for production and more!

<a name="setup-backend-development-environment"></a>
## Setup backend development environment

<a name="docker"></a>
### Dockerized environment

If you wish to use a dockerized development environment, you can easily do so by following these steps:

1. Add `.env` file:

    `cp .env.dev.sample .env`

2. Start local development environment:

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

1. Build images again with `make build`or `make build c=app`// or `c=test`

2. Stop and remove your environment with `make restart`. Even though continers are removed, your database volume will be preserved.

#### Recreate database

If you want to recreate the database:

1. Delete everything including volumes with `make purge`

2. Restart everything with `make up` (or `make server` for detached mode)

<a name="local-venv"></a>
### Local environment

#### Install

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

#### Run
With the venv activate it, execute:

`python manage.py collectstatic`

*Note* : Collect static is not necessary when debug is True (in dev mode)

Create initial database:

`python manage.py migrate`


Load demo data (optional):

`python manage.py loaddata demo`

Run server:

`python manage.py runserver 0.0.0.0:8000`

<a name="screenshots"></a>
## Screenshots

### Home page
<img src="screenshots/one.png" height="800">

### Add new position as employer
<img src="screenshots/two.png" height="800">

### Job details
<img src="screenshots/three.png" height="800">
