# Activity League

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
![Python](https://img.shields.io/pypi/pyversions/django)
![Coverage](./coverage.svg)
[![Unit Testing CI](https://github.com/UCLComputerScience/COMP0016_2020_21_Team19/actions/workflows/unit-testing.yml/badge.svg)](https://github.com/UCLComputerScience/COMP0016_2020_21_Team19/actions/workflows/unit-testing.yml)
[![Integration Testing CI (Chrome)](https://github.com/UCLComputerScience/COMP0016_2020_21_Team19/actions/workflows/integration-testing-chrome.yml/badge.svg)](https://github.com/UCLComputerScience/COMP0016_2020_21_Team19/actions/workflows/integration-testing-chrome.yml)
[![Integration Testing CI (Firefox)](https://github.com/UCLComputerScience/COMP0016_2020_21_Team19/actions/workflows/integration-testing-firefox.yml/badge.svg)](https://github.com/UCLComputerScience/COMP0016_2020_21_Team19/actions/workflows/integration-testing-firefox.yml)
[![Publish Docker image](https://github.com/UCLComputerScience/COMP0016_2020_21_Team19/actions/workflows/publish.yml/badge.svg)](https://github.com/UCLComputerScience/COMP0016_2020_21_Team19/actions/workflows/publish.yml)

Increasingly, hospitals are being mandated to monitor patient wellbeing post-treatment through Patient Reported Outcome Measures (PROMs). The NHS currently distributes a combination of paper and digital PROMs and suffer numerous delays before they can extract useful information from them. Currently, the process of collecting and analysing these measures can take up to a year to finalise. 

Under the [UCL Industry Exchange Network](https://www.ucl.ac.uk/computer-science/collaborate/ucl-industry-exchange-network-ucl-ixn) (UCL IXN) and with support from [NHS Wales](https://www.wales.nhs.uk/), we've developed a generalized web application enabling clinicians to quickly gather PROM data per individual and allow them to visualise and analyse the factors that help and hinder an individual from adherence to set treatment plans. Surveyors can create new tasks and add questions with different response types. Our platform provides visualisations for the responses to these tasks. 

Our solution dramatically reduces the time taken to collect and analyse responses to PROMs and may allow them to uncover health-related issues that would have gone undiscovered if assessed purely on the existing patient consultation framework. 

## Development

This section will describe how to get started with development on your local machine.
Refer to the [Deployment](#deployment) section for instructions on how to deploy Activity League.

Documentation for Activity League can be found [here](students.cs.ucl.ac.uk/2020/group19/docs).

### Getting Started

You will need to have [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed.

1. Clone this repo and `cd` into the cloned folder.
    `git clone https://github.com/UCLComputerScience/COMP0016_2020_21_Team19`
    
    `cd COMP0016_2020_21_Team19`

2. Since the repository has been created with use of a VCS such as git in mind, a secrets folder is required to avoid using and committing sensitive information (such as API keys) in code. Create a `secrets/` folder containing the following files:
   * `DB_USER` - database user
   * `DB_PASSWORD` - database password
   * `EMAIL_HOST` - email provider server name
   * `EMAIL_HOST_USER` - an email address
   * `EMAIL_HOST_PASSWORD` - password of above email address
   * `GOOGLE_CLIENT_ID` - Google API client ID
   * `GOOGLE_SECRET` - Google API secret key ID
   * `SECRET_KEY` - Django production key

   Each file should contain a single line containing the corresponding secret token.
   
   Only the `DB_PASSWORD` and `DB_USER`, and `SECRET_KEY` are strictly required. Read more about the secret key here [here](https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/
). If you don't need an email backend during development, you can use the following setting in [`settings.py`](ActivityLeague/settings.py) and not create the `EMAIL_HOST` `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` secrets.
   
   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
   ```
   
   If you don't intend on using Google SSO, you can also ignore the `GOOGLE*` secrets.
   
   Note: **You will need to modify the [`docker-compose.yml`](docker-compose.yml) and [`settings.py`](ActivityLeague/settings.py) files in accordance with the secrets you intend on using.**
3. Run `docker-compose build` to build the image. This will make the database migrations and install all dependencies.
4. Run `docker-compose up`. This will start the application on `localhost:8000`.
   > The application will have no data to begin with. If you wish to populate the database with some dummy data, simply run the `init-db.sh` script from within the container using
   ```
   docker-compose run web bash -c "./init-db.sh"
   ```
   This will create users on the platform and you can log in as one of them using the details below:
   > - Surveyor
   >    - email: `christine@black.com`
   >    - password: `activityleague`
   > - Respondent:
   >    - email: `john@doe.com`
   >    - password: `activityleague`
   > - Django admin:
   >    - username: `admin`
   >    - password: `activityleague`

Since this is a Django app, it is recommended to familiarise yourself with the [documentation](https://docs.djangoproject.com/en/3.1/) before proceeding with development.

### Testing

#### Unit

The unit testing suite for this project uses Django's built in testing library.

```python
from django.test import TestCase
```

The [coverage](https://coverage.readthedocs.io/en/coverage-5.5/) module is used to generate coverage reports.

To run the unit tests, simply execute the `test.sh` script from within the container using
```
docker-compose run web bash -c "./test.sh"
```

This will run the tests and provide a statement coverage summary in the command line. A directory named `htmlcov` will also be generated containing html files which can be viewed in a browser.

Run

```
python -m http.server 8080 -d htmlcov
```

to view the coverage report in your browser on `localhost:8080`.

The unit tests are located in the `tests/` directory within each app ([`authentication`](./authentication), [`core`](./core), [`respondent`](./respondent), [`surveyor`](./surveyor)).

#### Integration

The unit testing suite for this project uses the testing framework [Cypress](https://www.cypress.io/).

![Cypress](https://uclcomputerscience.github.io/COMP0016_2020_21_Team19/assets/cypress.gif)

To use Cypress, you will need to have [Node.js](https://nodejs.org/en/) installed. Follow [these](https://docs.cypress.io/guides/getting-started/installing-cypress#System-requirements) instructions to install the necessary requirements.

To run the tests, simply navigate to the [`integration_tests`](./integration_tests) directory and run the following commands.

`npm install` – to install the required Cypress dependencies

`npm run cypress:run` – to launch the Cypress app and run the tests in the GUI. If you would like to run the tests in headless mode with the output being shown in the command line, use `npx` instead of `npm`.

Cypress is a very extensive framework and more information about configuration and usage can be found [here](https://docs.cypress.io/guides/overview/why-cypress).

The integration tests can be found in the [`integration_tests/cypress/integration`](./integration_tests/cypress/integration) directory.

### Repository Structure

```
.
├── ActivityLeague                          # Contains Django specific configuration files
│   ├── asgi.py                             # ASGI config for the Django project.
│   ├── settings.py                         # Django settings.
│   ├── urls.py                             # URLs used in the project are defined here. Each URL
│   │                                         also points to an associated view, which is accessible in
│   │                                         views.py and is responsible for rendering the template.
│   └── wsgi.py                             # WSGI config for the Django project.
├── Dockerfile                              # Dockerfile using base Python image
├── LICENSE                                 # AGPL3 License
├── authentication                          # Django app containing code handling authentication.
│   ├── apps.py                             # Configuration for authentication-specific attributes.
│   ├── forms.py                            # Contains code for the signup and login forms.
│   ├── models.py                           # Defines authentication-specific database tables.
│   ├── signals.py                          # Contains code handling signals fired during authentication.
│   ├── tests/                              # Tests for the authentication app.
│   └── views.py                            # Views for each URL are defined here. Each view corresponds
│                                             to a URL and handles GET / POST requests.
├── core                                    # Django app containing code handling core functionality
│   │                                         which is also used by other apps.
│   ├── adapter.py                          # Defines a custom configuration for invitations backend.
│   ├── admin.py                            # Configuration used to display models in the Django admin panel.
│   ├── apps.py                             # Configuration for core-specific attributes.
│   ├── forms.py                            # Contains code for all forms used by both the surveyor
│   │                                         and respondent apps.
│   ├── models.py                           # Defines core-specific database tables.
│   ├── tests/                              # Tests for the authentication app.
│   ├── utils.py                            # Utility methods used by both the surveyor and respondent apps.
│   └── views.py                            # Views shared among surveyor and respondent apps are defined here.
├── docker-compose-production-example.yml   # Example Docker Compose configuration for use in deployment.
├── docker-compose.yml                      # Docker Compose configuration for use in development.
├── docs/                                   # Sphinx-generated reStructuredText documentation.
├── docs.sh                                 # Shell script to generate html from docstrings. Recommended
│                                             use is from within the 'web' Docker container.
├── init_db.py                              # Python script to populate the database with dummy data.
│                                             Should be used indirectly via 'init_db.sh' script.
├── init_db.sh                              # Bash script to execute 'init_db.py' after setting environment
│                                             variables correctly. Should be used from within the
│                                             'web' Docker container.
├── integration_tests                       # Integration tests for the project.
├── manage.py                               # Django project management utility.
├── requirements.txt                        # Contains a list of Python packages required by this project. 
├── respondent                              # Django app containing code handling functionality relating
│   │                                         to respondents.
│   ├── admin.py                            # Configuration used to display models in the Django admin panel.
│   ├── apps.py                             # Configuration for respondent-specific attributes.
│   ├── handler.py                          # Handles complex GET and all POST requests made to respondent views.
│   ├── models.py                           # Defines respondent-specific database tables.
│   ├── tests/                              # Tests for the authentication app.
│   └── views.py                            # Views for each URL are defined here. Each view corresponds
│                                             to a URL and handles GET / POST requests.
├── setup.cfg                               # Configuration for unit tests to exclude certain files from coverage.
├── start.sh                                # Docker container entrypoint file.
├── static/                                 # Contains CSS/JS files and assets.
├── surveyor                                # Django app containing code handling functionality relating
│   │                                         to surveyors.
│   ├── admin.py                            # Configuration used to display models in the Django admin panel.
│   ├── apps.py                             # Configuration for surveyor-specific attributes.
│   ├── forms.py                            # Contains code for all surveyor facing forms.
│   ├── handler.py                          # Handles complex GET and all POST requests made to surveyor views.
│   ├── models.py                           # Defines surveyor-specific database tables.
│   ├── tests/                              # Tests for the surveyor app.
│   ├── utils.py                            # Surveyor-specific utility methods.
│   └── views.py                            # Views for each URL are defined here. Each view corresponds
│                                             to a URL and handles GET / POST requests.
├── templates                               # Contains HTML for all the pages that the project uses.
│   ├── account                             # Pages used during authentication-related processes.
│   ├── base.html                           # Page defining basic layout used by all pages in
│   │                                         surveyor/ and respondent/.
│   ├── invitations                         # Pages used during invitation-related processes.
│   ├── respondent                          # Contains only respondent facing pages.
│   └── surveyor                            # Contains only surveyor facing pages.
└── test.sh                                 # Shell script to run unit tests. Should be used from within
                                              the 'web' Docker container. 
```

## Deployment

These instructions should be followed on a production server.

### Install Docker and Docker Compose by following the official instructions:

- Docker: [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)
- Docker Compose: [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)

### Starting the web app

Create a new directory called `deploy` in the `$HOME` directory.

Copy the following [`docker-compose-production-example.yml`](docker-compose-production-example.yml) into `~/deploy/`.

This file manages all the images and containers that the app requires.

```yaml
version: "3.9"

services:
  db:
    image: postgres
    environment:
      POSTGRES_DB: postgres
      POSTGRES_USER: {{ POSTGRES_USER }}
      POSTGRES_PASSWORD: {{ POSTGRES_PASSWORD }}
    volumes:
      - postgres_data:/var/lib/postgresql/data/
  web:
    image: docker.pkg.github.com/uclcomputerscience/comp0016_2020_21_team19/activityleague_web:latest
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      DB_USER: {{ POSTGRES_USER }}
      DB_PASSWORD: {{ POSTGRES_PASSWORD }}
      DEBUG: "False"
      EMAIL_HOST: {{ MAILSERVER.COM }}
      EMAIL_HOST_PASSWORD: {{ EMAIL_HOST_PASSWORD }}
      EMAIL_HOST_USER: {{ EMAIL_HOST_USER }}
      GOOGLE_CLIENT_ID: {{ GOOGLE_CLIENT_ID }}
      GOOGLE_SECRET: {{ GOOGLE_SECRET }}
      SECRET_KEY: {{ SECRET_KEY }}
  watchtower: # optional
    image: containrrr/watchtower
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /home/host/.docker/config.json:/config.json
    command: --interval 30
volumes:
  postgres_data:
```

This is an example `docker-compose.yml` that can be used on a production server.
The environment variables defined under the `web` service are used in `ActivityLeague/settings.py` and can be configured as your deployed instance requires.

The `watchtower` service is used to continuously check GitHub Packages for a newer build of the image and if it finds one, the new image is pulled and deployed. This service is optional

### Configuring the server to run Activity League on reboot

To run Activity League on server reboot automatically, create a file called `activity_league.service` in `/etc/systemd/system` and populate it with the following:

```ini
[Unit]
Description=Activity league docker compose deployment

[Service]
User={USERNAME}
Group=docker
WorkingDirectory=/home/{USERNAME}/deploy

ExecStartPre=/usr/local/bin/docker-compose pull --quiet
ExecStart=/usr/local/bin/docker-compose up

ExecStop=/usr/local/bin/docker-compose down

ExecReload=/usr/local/bin/docker-compose pull --quiet
ExecReload=/usr/local/bin/docker-compose down
ExecReload=/usr/local/bin/docker-compose up

[Install]
WantedBy=multi-user.target
```

Change `USERNAME` to whichever user is being used to deploy Activity League.

After you've copied this, save and close the file.

- Run `sudo systemctl daemon-reload` to allow the system to recognise the new service and once you've done this.
- Run `sudo systemctl enable activity_league` to ensure that the service runs automatically at startup.
- To get it up and running now, run `sudo systemctl activity_league start`.

### Manual Deployment

The steps described above will set up a continuous deployment workflow.

If this type of deployment is undesirable, you can simply omit the `watchtower` service from the `docker.compose.yml`.

The image running on the server can then be updated only by:

- SSH-ing into the server as the user being used to deploy Activity League.
- Navigating to `~/deploy`.
- Running `docker-compose down` to stop the web app.
- Running `docker-compose build` to rebuild the containers using the latest images.
- Running `docker-compose up -d` to run the web app on port 8000 in detached mode (i.e. in the background).