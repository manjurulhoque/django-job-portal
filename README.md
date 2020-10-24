<h1 align="center">Anem per feina</h1>
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->

[![All Contributors](https://img.shields.io/badge/all_contributors-18-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
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
* [Contributors](#contributors)

<a name="the-project"></a>
## The project

The objective of this _hackathon_ is to launch a **job portal website** where tech community can find _curated_ job opportunities from local companies.

We forked the open source project [django-job-portal](https://github.com/manjurulhoque/django-job-portal) (See [demo 1](https://django-portal.herokuapp.com/), [demo 2](http://jobs.manjurulhoque.com/)) and use it as a baseline.

<a name="deployment"></a>
## Deployment

### Kubernetes deployment

To deploy to a k8s cluster see the [k8s manifests](/manifests/README.md)

<a name="contributing"></a>
## Contributing

**Anem per feina** is a collaborative effort where everybody is more than welcome to contribute, no experience is required!

Have a look at [CONTRIBUTING.md](CONTRIBUTING.md) file that describes the process to submit a contribution, and come say hi 👋👋 to [GeeksCat slack](https://geekscat.slack.com) where most contributors hang out.

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

1.With the venv activate it, execute:

    `python manage.py collectstatic`

*Note* : Collect static is not necessary when debug is True (in dev mode)

2. Create initial database:

    `python manage.py migrate`


3. Load demo data (optional):

    `python manage.py loaddata demo`

4. Run server:

    `python manage.py runserver 0.0.0.0:8000`

<a name="contributors"></a>
## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="http://xaviertorello.cat/"><img src="https://avatars3.githubusercontent.com/u/8709244?v=4?s=80" width="80px;" alt=""/><br /><sub><b>Xavi Torelló</b></sub></a><br /><a href="#question-XaviTorello" title="Answering Questions">💬</a> <a href="https://github.com/GeeksCat/anem-per-feina/commits?author=XaviTorello" title="Code">💻</a> <a href="https://github.com/GeeksCat/anem-per-feina/commits?author=XaviTorello" title="Documentation">📖</a> <a href="#eventOrganizing-XaviTorello" title="Event Organizing">📋</a> <a href="#ideas-XaviTorello" title="Ideas, Planning, & Feedback">🤔</a> <a href="#infra-XaviTorello" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="#mentoring-XaviTorello" title="Mentoring">🧑‍🏫</a> <a href="#projectManagement-XaviTorello" title="Project Management">📆</a> <a href="https://github.com/GeeksCat/anem-per-feina/pulls?q=is%3Apr+reviewed-by%3AXaviTorello" title="Reviewed Pull Requests">👀</a></td>
    <td align="center"><a href="https://github.com/jbagot"><img src="https://avatars1.githubusercontent.com/u/11691527?v=4?s=80" width="80px;" alt=""/><br /><sub><b>Jordi Bagot Soler</b></sub></a><br /><a href="#question-jbagot" title="Answering Questions">💬</a> <a href="https://github.com/GeeksCat/anem-per-feina/commits?author=jbagot" title="Code">💻</a> <a href="https://github.com/GeeksCat/anem-per-feina/commits?author=jbagot" title="Documentation">📖</a> <a href="#eventOrganizing-jbagot" title="Event Organizing">📋</a> <a href="#ideas-jbagot" title="Ideas, Planning, & Feedback">🤔</a> <a href="#infra-jbagot" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="#mentoring-jbagot" title="Mentoring">🧑‍🏫</a> <a href="#projectManagement-jbagot" title="Project Management">📆</a> <a href="https://github.com/GeeksCat/anem-per-feina/pulls?q=is%3Apr+reviewed-by%3Ajbagot" title="Reviewed Pull Requests">👀</a></td>
    <td align="center"><a href="https://github.com/francescarpi"><img src="https://avatars0.githubusercontent.com/u/287872?v=4?s=80" width="80px;" alt=""/><br /><sub><b>Francesc Arpí Roca</b></sub></a><br /><a href="#question-francescarpi" title="Answering Questions">💬</a> <a href="https://github.com/GeeksCat/anem-per-feina/issues?q=author%3Afrancescarpi" title="Bug reports">🐛</a> <a href="https://github.com/GeeksCat/anem-per-feina/commits?author=francescarpi" title="Code">💻</a> <a href="https://github.com/GeeksCat/anem-per-feina/commits?author=francescarpi" title="Documentation">📖</a> <a href="#eventOrganizing-francescarpi" title="Event Organizing">📋</a> <a href="#ideas-francescarpi" title="Ideas, Planning, & Feedback">🤔</a> <a href="#mentoring-francescarpi" title="Mentoring">🧑‍🏫</a> <a href="#projectManagement-francescarpi" title="Project Management">📆</a> <a href="https://github.com/GeeksCat/anem-per-feina/pulls?q=is%3Apr+reviewed-by%3Afrancescarpi" title="Reviewed Pull Requests">👀</a></td>
    <td align="center"><a href="https://github.com/d-asensio"><img src="https://avatars2.githubusercontent.com/u/13970905?v=4?s=80" width="80px;" alt=""/><br /><sub><b>David Asensio Cañas</b></sub></a><br /><a href="#question-d-asensio" title="Answering Questions">💬</a> <a href="https://github.com/GeeksCat/anem-per-feina/issues?q=author%3Ad-asensio" title="Bug reports">🐛</a> <a href="https://github.com/GeeksCat/anem-per-feina/commits?author=d-asensio" title="Code">💻</a> <a href="#design-d-asensio" title="Design">🎨</a> <a href="https://github.com/GeeksCat/anem-per-feina/commits?author=d-asensio" title="Documentation">📖</a> <a href="#eventOrganizing-d-asensio" title="Event Organizing">📋</a> <a href="#ideas-d-asensio" title="Ideas, Planning, & Feedback">🤔</a> <a href="#mentoring-d-asensio" title="Mentoring">🧑‍🏫</a> <a href="https://github.com/GeeksCat/anem-per-feina/pulls?q=is%3Apr+reviewed-by%3Ad-asensio" title="Reviewed Pull Requests">👀</a></td>
    <td align="center"><a href="https://www.victormartingarcia.com/"><img src="https://avatars1.githubusercontent.com/u/659832?v=4?s=80" width="80px;" alt=""/><br /><sub><b>Victor</b></sub></a><br /><a href="https://github.com/GeeksCat/anem-per-feina/commits?author=victormartingarcia" title="Code">💻</a> <a href="https://github.com/GeeksCat/anem-per-feina/commits?author=victormartingarcia" title="Documentation">📖</a> <a href="#eventOrganizing-victormartingarcia" title="Event Organizing">📋</a> <a href="#ideas-victormartingarcia" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/GeeksCat/anem-per-feina/pulls?q=is%3Apr+reviewed-by%3Avictormartingarcia" title="Reviewed Pull Requests">👀</a></td>
    <td align="center"><a href="https://github.com/fullonic"><img src="https://avatars3.githubusercontent.com/u/13336073?v=4?s=80" width="80px;" alt=""/><br /><sub><b>dbf</b></sub></a><br /><a href="https://github.com/GeeksCat/anem-per-feina/commits?author=fullonic" title="Code">💻</a> <a href="https://github.com/GeeksCat/anem-per-feina/pulls?q=is%3Apr+reviewed-by%3Afullonic" title="Reviewed Pull Requests">👀</a></td>
    <td align="center"><a href="https://github.com/ytturi"><img src="https://avatars2.githubusercontent.com/u/8191681?v=4?s=80" width="80px;" alt=""/><br /><sub><b>Ytturi</b></sub></a><br /><a href="https://github.com/GeeksCat/anem-per-feina/commits?author=ytturi" title="Code">💻</a> <a href="#ideas-ytturi" title="Ideas, Planning, & Feedback">🤔</a> <a href="#infra-ytturi" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/GeeksCat/anem-per-feina/pulls?q=is%3Apr+reviewed-by%3Aytturi" title="Reviewed Pull Requests">👀</a></td>
    <td align="center"><a href="https://github.com/dguillen12"><img src="https://avatars0.githubusercontent.com/u/71018943?v=4?s=80" width="80px;" alt=""/><br /><sub><b>Didac Guillen</b></sub></a><br /><a href="https://github.com/GeeksCat/anem-per-feina/commits?author=dguillen12" title="Code">💻</a> <a href="#infra-dguillen12" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/xdiume"><img src="https://avatars1.githubusercontent.com/u/72464185?v=4?s=80" width="80px;" alt=""/><br /><sub><b>xdiume</b></sub></a><br /><a href="https://github.com/GeeksCat/anem-per-feina/commits?author=xdiume" title="Code">💻</a></td>
    <td align="center"><a href="https://avatars.githubusercontent.com/u/6842807"><img src="https://avatars2.githubusercontent.com/u/6842807?v=4?s=80" width="80px;" alt=""/><br /><sub><b>Xavier Marquès</b></sub></a><br /><a href="https://github.com/GeeksCat/anem-per-feina/commits?author=wolframtheta" title="Code">💻</a></td>
    <td align="center"><a href="https://www.linkedin.com/in/castellinmanuel/"><img src="https://avatars2.githubusercontent.com/u/2655072?v=4?s=80" width="80px;" alt=""/><br /><sub><b>Manuel Castellin</b></sub></a><br /><a href="https://github.com/GeeksCat/anem-per-feina/commits?author=mcastellin" title="Code">💻</a> <a href="#infra-mcastellin" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/GeeksCat/anem-per-feina/pulls?q=is%3Apr+reviewed-by%3Amcastellin" title="Reviewed Pull Requests">👀</a></td>
    <td align="center"><a href="https://github.com/oriolpiera"><img src="https://avatars2.githubusercontent.com/u/26488435?v=4?s=80" width="80px;" alt=""/><br /><sub><b>Oriol Piera</b></sub></a><br /><a href="https://github.com/GeeksCat/anem-per-feina/commits?author=oriolpiera" title="Code">💻</a></td>
    <td align="center"><a href="http://www.tecob.com/"><img src="https://avatars3.githubusercontent.com/u/2232647?v=4?s=80" width="80px;" alt=""/><br /><sub><b>Franc Rodriguez</b></sub></a><br /><a href="#infra-francrodriguez" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
    <td align="center"><a href="https://stackoverflow.com/users/842935/danihp?tab=profile"><img src="https://avatars2.githubusercontent.com/u/3105983?v=4?s=80" width="80px;" alt=""/><br /><sub><b>dani herrera</b></sub></a><br /><a href="https://github.com/GeeksCat/anem-per-feina/commits?author=ctrl-alt-d" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/mcmontseny"><img src="https://avatars0.githubusercontent.com/u/72517550?v=4?s=80" width="80px;" alt=""/><br /><sub><b>Marc Casamitjana Montseny</b></sub></a><br /><a href="https://github.com/GeeksCat/anem-per-feina/commits?author=mcmontseny" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/lluisd"><img src="https://avatars3.githubusercontent.com/u/7629843?v=4?s=80" width="80px;" alt=""/><br /><sub><b>lluisd</b></sub></a><br /><a href="https://github.com/GeeksCat/anem-per-feina/commits?author=lluisd" title="Code">💻</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/eudago"><img src="https://avatars2.githubusercontent.com/u/809916?v=4?s=80" width="80px;" alt=""/><br /><sub><b>Eudald Dachs</b></sub></a><br /><a href="https://github.com/GeeksCat/anem-per-feina/commits?author=eudago" title="Code">💻</a></td>
    <td align="center"><a href="https://www.linkedin.com/in/ericmassip/"><img src="https://avatars3.githubusercontent.com/u/22151914?v=4?s=80" width="80px;" alt=""/><br /><sub><b>Eric Massip</b></sub></a><br /><a href="https://github.com/GeeksCat/anem-per-feina/commits?author=ericmassip" title="Code">💻</a> <a href="#infra-ericmassip" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
